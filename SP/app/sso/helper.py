from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings

from fastapi import Request, HTTPException

from app.sso import db as sso_db
from config import deploy_config
from app.model import User

# Load the SAML settings
saml_settings = OneLogin_Saml2_Settings(settings=deploy_config.get("sso_settings", None))


async def get_current_user(request: Request) -> User:
    '''Check session for user info'''
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None
    session = await sso_db.get_session_by_id(session_id)
    if not session:
        return None
    return session.user

async def authenticate_user(request: Request) -> User:
    user = await get_current_user(request)
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
    

def get_sso_login_redirect_url(request: Request) -> str:
    saml_auth = OneLogin_Saml2_Auth(request, saml_settings)
    # saml_auth.login() returns a redirect URL to the SSO login page provided by the IdP
    return saml_auth.login(return_to=str(request.url))


async def process_login_assertion(request: Request) -> str | None:
    saml_auth = OneLogin_Saml2_Auth(request, saml_settings)
    saml_auth.process_response()
    errors = saml_auth.get_errors()
    if errors:
        return None
    user_info = saml_auth.get_attributes()
    # Create session in database
    return await sso_db.create_session(user_info)


async def process_logout_assertion(request: Request):
    '''Process logout assertion from IdP'''
    ## When receiving a logout assertion, there are two ways to delete the session
    ## We use both to ensure the session is deleted
    
    # 1. Delete the session by session ID
    await sso_db.delete_session_by_id(request.cookies.get("session_id"))
    
    # 2. Delete the session by user info extracted from the assertion
    saml_auth = OneLogin_Saml2_Auth(request, saml_settings)
    saml_auth.process_slo()
    user_info = saml_auth.get_attributes()
    user = User(**user_info)
    await sso_db.delete_session_by_user(user)
    return