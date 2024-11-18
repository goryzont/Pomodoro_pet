from app.handlers.tasks import router as tasks_router
from app.handlers.ping import router as ping_router
from app.handlers.categories import router as categories_router
from app.handlers.user import router as user_router
from app.handlers.auth import router as auth_router

routers = [tasks_router, ping_router, categories_router, user_router, auth_router]