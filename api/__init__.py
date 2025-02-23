from fastapi import APIRouter

from api.todo import router as todo_router


router = APIRouter()

router.include_router(todo_router)
