from fastapi import FastAPI
from controllers.user_controller import router as usuario_router
from controllers.auth_controller import router as auth_router 

app = FastAPI()

app.include_router(usuario_router)
app.include_router(auth_router)

