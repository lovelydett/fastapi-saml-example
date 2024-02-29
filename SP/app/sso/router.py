from fastapi import APIRouter, Request, responses
from app.model import User

from .helper import get_current_user, get_sso_login_redirect_url, process_login_assertion, process_logout_assertion

api = APIRouter(prefix="sso", tags=["sso"])


@api.get("/login")
async def login(request: Request):
    '''Login user'''
    user = await get_current_user(request)
    if user is not None:
        return 200, {"message": "Already logged in"}
    # Redirect to SSO login
    redirect_url = get_sso_login_redirect_url(request)
    return responses.RedirectResponse(redirect_url)


@api.post("/acs")
async def acs(request: Request, response: responses.Response):
    '''Assertion Consumer Service'''
    session_id = process_login_assertion(request)
    if session_id is None:
        return 401, {"message": "Unauthorized"}

    response.set_cookie("session_id", session_id)
    return 200, {"message": "Logged in"}


@api.post("/slo")
async def slo(request: Request, response: responses.Response):
    '''Single Logout'''
    process_logout_assertion(request)
    response.delete_cookie("session_id")
    return 200, {"message": "Logged out"}
