from routes.Routes import router
from fastapi import FastAPI
from config.Database import DataBase

app = FastAPI(docs_url=None,
        redoc_url=None,
        openapi_url=None  )

@app.on_event("startup")
async def startup_db():
    print("FastAPI is Starting up")
    DataBase

# Close the database connection on shutdown
@app.on_event("shutdown")
async def shutdown_db():
    print("FastAPI is shutting down")

app.include_router(router)
