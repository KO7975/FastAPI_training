import uvicorn
from fastapi import FastAPI
from database import engine
import models
from routers.user import router
from routers.user_details import router as router1


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router, prefix='/user')
app.include_router(router1, prefix='/user_details')


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=3)