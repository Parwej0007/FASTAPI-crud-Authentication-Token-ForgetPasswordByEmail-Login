from fastapi import FastAPI, Depends, status, Response, HTTPException
# from blog import sc
from . import schemas_d, hashing, token, reset_password_with_eamil
from . import models
from .database import engine, sessionLocal
from sqlalchemy.orm import Session
from typing import List
from . import oauth2
from fastapi.security import OAuth2PasswordRequestForm
import uuid
#for generete reset code

# debug
# from traceback import format_exc as _format_exc


# connecting db and for create table inside database
# Migrating all the table --> models.Base_db.metadata.create_all(bind=engine)
models.Base_db.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    except Exception as e:
        return {"errors": e}
    finally:
        db.close()



app = FastAPI()


############# CRUD blog using fastapi and use database - PostgreSQL ###################

# create_blog()
@app.post('/blog/create/', status_code=status.HTTP_201_CREATED, tags=["blog"])
def create_blog(request: schemas_d.BlogCreate, db: Session = Depends(get_db)):
    # request: sc.BlogCreate call pydantic for validate request

    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'Created Blog': f"{new_blog.title}"}


# fecth all data from blog show
# now using authentication token for access post current_user
@app.get('/blog/list/', status_code=status.HTTP_200_OK, tags=["blog"], )
def show_blog(db: Session = Depends(get_db), current_user: schemas_d.ListSchemaUser = Depends(oauth2.get_current_user)):
    all_blog = db.query(models.Blog).all()
    return {"data": all_blog}

# details data from blog
@app.get('/blog/details/{id}/', status_code= status.HTTP_200_OK, response_model=schemas_d.ShowBlog, tags=["blog"])
def details_blog(id: int, db: Session = Depends(get_db)):
    fetch_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    print(fetch_blog.user_id)
    # if not fetch data
    if not fetch_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data": "Not Found"}
    else:
        return fetch_blog


# update blog
@app.put('/blog/update/{id}/', status_code=status.HTTP_202_ACCEPTED, tags=["blog"])
def update_blog(id: int, request: schemas_d.BlogCreate, db: Session = Depends(get_db)):
    fetch_blog = db.query(models.Blog).filter(models.Blog.id==id)
    if fetch_blog.first(): # get first fetch data
        fetch_blog.update(request)
        db.commit()
        return {"Update": f"id {id} is Updated"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found id {id}")


# delete blog post
@app.delete('/blog/delete/{id}/', status_code=status.HTTP_204_NO_CONTENT, tags=["blog"])
def delete_post(id: int, db: Session = Depends(get_db)):
    fetch = db.query(models.Blog).filter(models.Blog.id==id).first()
    if fetch:
        fetch.delete()
        db.commit()
        return {"delete": f"id {id} is deleted "}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not content found")


################################### END CRUD #####################################


# This is using to show only needed data (what we want to show)- use-> response_model=List[sc.BlogCreateResponse]
# use response for a pydantic model -> when we want to show(response) column according to need
# we use response_model inside the path

# fecth all data from blog show
@app.get('/blog/list/response_model_use/', status_code=status.HTTP_200_OK, response_model=List[schemas_d.BlogCreateResponse], tags=["blog"])
def show_blog_res(db: Session = Depends(get_db)):
    all_blog = db.query(models.Blog).all()
    # return {"data":all_blog} giving intervel server error
    return all_blog







######################################## service user ############################### start ###########
# create user

@app.post("/user/create/", status_code=status.HTTP_201_CREATED, tags=["user"])
def create_user(user_schema: schemas_d.CreateUserSchema, db: Session = Depends(get_db)):

    user_data_dict = user_schema.dict()
    if user_data_dict['password1'] != user_data_dict['password2']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Password1 is not matched to Password2')
    else:
        # hassing password
        user_data = models.UserModel(username=user_schema.username, email=user_schema.email,
                                     password=hashing.HashPassword.bcrypt(user_schema.password1),  # call hash class
                                     first_name=user_schema.first_name, last_name=user_schema.last_name)
        print(user_data)
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        return user_data

@app.get("/user/list", status_code=status.HTTP_200_OK, response_model=List[schemas_d.ListSchemaUser], tags=['user'])
def user_list(db: Session = Depends(get_db)):
    data = db.query(models.UserModel).all()
    return data





########################## login user ########################
# Login for access token OAuth2PasswordRequestForm = Depends()

@app.post("/user/login/", status_code=status.HTTP_202_ACCEPTED, tags=["user"])
def login(request_schema: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
                                                                    # request_schema.username is basically email
    user = db.query(models.UserModel).filter(models.UserModel.email == request_schema.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invailid Credentail")

    if not hashing.HashPassword.verify_pass(request_schema.password, user.password) : # old password and hash password
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invailid Password")

    # generate a JWT token and return
    access_token = token.create_access_token(data={"sub": user.email} )

    return {"access_token": access_token, "token_type": "bearer"}






#################### Forget password by email ########################

@app.post("/user/password/forget/", status_code=status.HTTP_200_OK, tags=['Password Forget'])
async def user_password_forget(request: schemas_d.UserPassForgetSchema, db: Session = Depends(get_db)):
    email= db.query(models.UserModel).filter(models.UserModel.email==request.email).first()
    if not email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email Does'nt exist")

    # create reset code abd save in database
    reset_code = str(uuid.uuid1())

    # insert email and reset code in reset_code db
    reset_data = models.ForgetPasswordId(email=request.email, reset_code=reset_code)
    db.add(reset_data)
    db.commit()
    db.refresh(reset_data)

    # sending mail
    subject = "forget password mail"
    recipient = [request.email]
    message = f"""
                <p> this is for forget password code {reset_code} </p>
                """

    await reset_password_with_eamil.send_mail(subject, recipient, message)

    return {"status": "ok"}






import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)