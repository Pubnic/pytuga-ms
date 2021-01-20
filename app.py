from random import randint
from mangum import Mangum
from typing import Dict
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


app = FastAPI(title=__name__)


@app.get('/')
async def get_index() -> Dict:
    return dict(status='OK')


@app.post('/')
async def post_index(data: Dict) -> Dict:
    return dict(id=randint(0, 99), **data), 201


@app.exception_handler(Exception)
async def handle_all_exceptions(request: Request, error: Exception):
    return JSONResponse(
        status_code=500,
        content=str(error),
    )


def handler(event, context):
    if event.get('multiValueQueryStringParameters', False) is False:
        event['multiValueQueryStringParameters'] = None

    asgi_handler = Mangum(app)
    response = asgi_handler(event, context)  # Call the instance with the event arguments

    return response
