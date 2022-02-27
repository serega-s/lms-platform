from fastapi import APIRouter
from ..api.auth import router as auth_router
from ..api.profile import router as profile_router

router = APIRouter(prefix='/api')
router.include_router(auth_router)
router.include_router(profile_router)