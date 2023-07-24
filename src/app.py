from fastapi import FastAPI, APIRouter

from src.menu import menu_router
from src.submenu import submenu_router

app = FastAPI()

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(menu_router.router)
router.include_router(submenu_router.router)

app.include_router(router)
