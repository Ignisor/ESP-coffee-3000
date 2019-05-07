from utils.pins import open_relay
from data import conf

from esp.utils.user_config import UserConfig
from . import server_app as srv
from .core import JSONResponse, Response


@srv.view('POST', '/')
def process_post(request):
    return JSONResponse(200, {"status": open_relay()})


@srv.view('GET', '/config/')
def get_config(request):
    return JSONResponse(200, UserConfig().get())


@srv.view('POST', '/config/')
def update_config(request):
    if not isinstance(request.body, dict):
        return Response(400, "400 Bad Request (request is not in JSON format)")

    user_conf = UserConfig()
    user_conf.update(request.body)

    return JSONResponse(200, user_conf.get())


@srv.view('GET', '/error/')
def get_error(request):
    with open(conf.ERROR_LOG_FILENAME) as error_log:
        resp = Response(200, error_log.read())

    return resp
