from fastapi import FastAPI
from mysite.admin.setup import setup_admin
from mysite.api import exhibits, auth, ai
import uvicorn


museum_app = FastAPI()

museum_app.include_router(exhibits.home_router)
museum_app.include_router(exhibits.exhibit_router)
museum_app.include_router(auth.auth_router)
museum_app.include_router(ai.ai_router)
setup_admin(museum_app)


if __name__ == '__main__':
    uvicorn.run(museum_app, host="127.0.0.1", port=8000)
