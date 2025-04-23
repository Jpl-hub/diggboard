import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse,StreamingResponse
from starlette.staticfiles import StaticFiles

from server.const import verify_token
from urls import router


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.split('/')[-1][0].islower() and 'static' not in request.url.path:
            token = request.headers.get('token')
            user = verify_token(token)

            request.state.user = user
            if user is None:
                return JSONResponse({'code': 401, 'message': '请重新登录'})

        response = await call_next(request)
        return response


middlewares = [
    Middleware(CORSMiddleware, allow_origins=['*']),
    Middleware(CustomMiddleware)

]

fast_app = FastAPI(middleware=middlewares)
fast_app.include_router(router, prefix='/api')

fast_app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    port = 7878
    uvicorn.run('main:fast_app', port=port, reload=True)
