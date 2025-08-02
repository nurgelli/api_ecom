from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import users, login, products
from fastapi.security import OAuth2PasswordBearer


print(settings.SECRET_KEY)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")



app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_extra={
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        },
        "security": [{"BearerAuth": []}]
    }
)

app.include_router(users.router, prefix=settings.API_V1_STR, tags=['users'])
app.include_router(login.router, prefix=settings.API_V1_STR, tags=['login'])
app.include_router(products.router, prefix=settings.API_V1_STR, tags=["products"])

@app.get('/')
async def root():
    return {"messages": "Welcome to FastAPI E-commerce API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)