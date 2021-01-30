import traceback
import sys
import contextlib
from io import StringIO
from mangum import Mangum
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pytuga import exec
from transpyler.translate.google_translate import GoogleTranslator


app = FastAPI(title=__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


class Body(BaseModel):
    code: str


class Response(BaseModel):
    response: str
    error: bool = False
    traceback: str = None


@app.post('/pytuga')
async def run(body: Body) -> Response:
    with stdoutIO() as s:
        try:
            exec(body.code)
            return Response(response=str(s.getvalue()))
        except Exception as ex:
            translator = GoogleTranslator('pt_BR')

            error_traceback = str(s.getvalue())
            traceback_translated = translator.google_translate(traceback.format_exc())
            error_traceback += traceback_translated

            error_message = translator.google_translate(str(ex))
            return Response(response=error_message, error=True, traceback=error_traceback)


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
