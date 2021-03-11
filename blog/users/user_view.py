
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
# from ..database import Base_db # .. for back from file
from .. import schemas
from ..database import sessionLocal, Base_db, engine
from .. import models
from . import hashing





# DATABASE table create
models.Base_db.metadata.create_all(bind=engine)

# create db connection for fetching data use session
def get_db():
    db = sessionLocal()
    try:
        yield db
    except Exception as e:
        return {"db error": e}
    finally:
        db.close()


# FastAPI instance
app = FastAPI()
#  cros middleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True, )



# create user
# after successfully created user we want to show anly user name and email as response we use response_model
# seperat methods we use tags=["name method for use"]
@app.post('/blog/user/', status_code=status.HTTP_201_CREATED, response_model=schemas.BlogUserResponseModel, tags=["Users"])
def create_user(request_user: schemas.BlogUser, db: Session = Depends(get_db)):
    email_f = request_user.email
    # filter email should be unique
    # filter_email = db.query(models.UserModel.email==email_f).first()
    # if not filter_email:
    user = models.UserModel(name=request_user.name, email=request_user.email, password=hashing.Hashing.bcrypt_pass(request_user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
    # else:
    #     raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email should be unique")



@app.get("/user/details/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    get_user = db.query(models.UserModel).filter(models.UserModel.id==id)
    if get_user:
        return get_user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)








# for debug host 9000
import uvicorn
#
# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=9000)

