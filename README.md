# fastapi-saml-example
Integrate SAML-based SSO into a FastAPI application.

## Overview
Recently, there was a new project that required SSO integration via SAML, and TL chose FastAPI as the backend framework. Given that neither has any prior experience, this repository is a test run for building the basic logic. It also provides a brief overview of SSO via SAML2.0 just for learning purpose.

## Layout
A SP implemented via FastAPI is in ```/SP```, and the ```/IdP``` provides a simple identity provider in Node.js just for testing.  
The main utilities of the SSO via SAML are included in ```/SP/app/sso```, and the three critical SAML endpoints are in ```/SP/app/sso/router.py```

## Deployment
### Launch IdP
### Launch SP
- ```cd /SP```
- ```python3.12 -m venv venv```
- ```pip install -r requirements.txt```
- ```uvicorn server:app --reload```

## Introduction to SAML-2.0