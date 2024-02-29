'''Define the FastAPI application and include routers'''

__author__ = "Yuting Xie"
__email__ = "xyt@bupt.cn"
__date__ = "2024/2/29"

from fastapi import FastAPI
from app.business_module_1 import module_1_router
from app.business_module_2 import module_2_router
from app.sso import sso_router

app = FastAPI()

app.include_router(module_1_router, tags=["module_1"])
app.include_router(module_2_router, tags=["module_2"])
app.include_router(sso_router, tags=["sso"])
