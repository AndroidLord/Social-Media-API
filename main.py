from fastapi import FastAPI
import models
from database import engine
from routers import post, user, auth
from config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

print(settings.database_port)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# Home Url
@app.get('/')
def root():
    return {"message": "Hello World"}


