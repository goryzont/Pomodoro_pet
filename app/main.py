from fastapi import FastAPI
from app.handlers import  routers

app = FastAPI(
    title='pomidoro-time',
    docs_url='/api/docs',
    description='Ручки помадоро таймера'
)

for router in routers:
    app.include_router(router)