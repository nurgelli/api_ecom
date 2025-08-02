from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import users, login

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(users.router, prefix=settings.API_V1_STR, tags=['users'])
app.include_router(login.router, prefix=settings.API_V1_STR, tags=['login'])

@app.get('/')
async def root():
    return {"messages": "Welcome to FastAPI E-commerce API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)