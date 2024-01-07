import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import JSONResponse

import sixsaudit_token.token
from controllers import (auth_controller, environment_controller, inspection_form_controller,
                         inspection_type_controller, user_controller, location_controller, inspection_target_controller)
from dotenv import load_dotenv
import uvicorn

app = FastAPI()

@app.middleware("http")  # Middleware to check CSRF tokens
async def check_csrf(request: Request, call_next):

    if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
        # Check CSRF tokens for POST, PUT, PATCH, and DELETE requests
        if str(request.url).find('login') == -1 and str(request.url).find('register') == -1:
            # Skip CSRF check for login and registration routes
            try:
                # Initialize and validate CSRF and access tokens
                _token = sixsaudit_token.token.init_token()
                csrf = _token.validate(request.cookies.get('csrf_token_cookie'))
                access = _token.validate(request.cookies.get('access_token_cookie'))
                if csrf is None or access is None:
                    return JSONResponse(content={'err': 'forbidden1'}, status_code=403)
                if csrf['sub'] != access['csrf']:
                    return JSONResponse(content={'err': 'forbidden2'}, status_code=403)
            except Exception as e:
                return JSONResponse(content={'err': 'forbidden3', 'status': str(e)}, status_code=403)
    response = await call_next(request)
    return response

# Set allowed origins
# Change this address to the address of your own frontend application
origins = [
    "http://localhost:3000",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all HTTP headers
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers for different controllers
app.include_router(auth_controller.router)
app.include_router(environment_controller.router)
app.include_router(inspection_form_controller.router)
app.include_router(inspection_target_controller.router)
app.include_router(inspection_type_controller.router)
app.include_router(location_controller.router)
app.include_router(user_controller.router)


if __name__ == '__main__':
    load_dotenv()
    if os.getenv('SSL') == '0':
        # Run the application without SSL
        uvicorn.run('main:app', port=8002, reload=True)
    elif os.getenv('SSL') == '1':
        # Run the application with SSL
        uvicorn.run('main:app', port=8002, reload=True, ssl_keyfile='./cert/CA/localhost/localhost.decrypted.key',
                    ssl_certfile='./cert/CA/localhost/localhost.crt')
