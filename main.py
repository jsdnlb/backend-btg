from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from database.db import create_tables
from routes.client import routes_client
from routes.fund import routes_fund
from routes.transaction import routes_transaction


app = FastAPI(title="Backend BTG - Swagger UI", version="0.1")

origins = [
    "http://frontend-btg-challenge-bucket.s3-website-us-east-1.amazonaws.com/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


""" @app.exception_handler(404)
def not_found(request, exc):
    return JSONResponse(status_code=404, content={"message": "Not Found"}) """


app.include_router(routes_client, prefix="/clients")
app.include_router(routes_fund, prefix="/funds")
app.include_router(routes_transaction, prefix="/transactions")

create_tables()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, reload=True)
