from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from data.models import Base
from data.db import engine
from controllers import include_router
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

include_router(app)

@app.get('/')
def home():
    html = '''
        <h1>Welcome to ecommerce api</h1>
        <p> To Use the api head to the <a href='/docs'>/docs</a> endpoint</p>
    '''

    return HTMLResponse(html, status_code=200)
if __name__ == "__main__":
    uvicorn.run(app)
