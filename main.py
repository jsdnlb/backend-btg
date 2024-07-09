from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from database.db import create_tables
from routes.client import routes_client
from routes.fund import routes_fund
from routes.transaction import routes_transaction


app = FastAPI(title="Backend BTG - Swagger UI", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(404)
def not_found(request, exc):
    return JSONResponse(status_code=404, content={"message": "Not Found"})


app.include_router(routes_client, prefix="/client")
app.include_router(routes_fund, prefix="/fund")
app.include_router(routes_transaction, prefix="/transaction")

create_tables()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
