from fastapi import FastAPI
from data.models import Base
from data.db import engine
from controllers import include_router
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

include_router(app)

if __name__ == "__main__":
    uvicorn.run(app)
