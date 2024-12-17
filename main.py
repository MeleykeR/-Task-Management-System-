import os
from fastapi import FastAPI, HTTPException, status, Query, Request, APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from contextlib import asynccontextmanager

# Database initialization
from helpers.db import DB

# Import services
from services.users import Users
from services.managers import Managers
from services.tasks import Tasks

# Import schemas
from schemas.user_input_output import *
from schemas.team_input_output import *
from schemas.manager_input_output import *
from schemas.task_input_output import *


# ========================= LIFESPAN EVENT =========================
@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize database when the app starts."""
    DB.init()
    yield


# ========================= APP INITIALIZATION =========================
app = FastAPI(
    title="Task Management API",
    version="1.0",
    lifespan=lifespan,
    description="API for managing tasks, users, teams, and managers.",
)


# ========================= GLOBAL EXCEPTION HANDLER =========================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, e: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"name": type(e).__name__, "message": str(e)},
    )


# ========================= ROOT PATH REDIRECT =========================
@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def root():
    return "/docs"


# ========================= ROUTERS =========================
def create_user_routes():
    router = APIRouter(prefix="/users", tags=["Users"])

    @router.post("/add")
    async def add_user(userData: UserInputAdd):
        return {"id": Users.addUser(userData)}

    @router.put("/update/{id}")
    async def update_user(id: int, userData: UserInputUpdate):
        return Users.updateUser(id, userData)

    @router.get("/search")
    async def search_users(
        id: int | None = Query(None, ge=0),
        name: str | None = Query(None, max_length=50),
        role: str | None = None,
        limit: int = Query(10, gt=0),
        offset: int = Query(0, ge=0),
    ) -> list[UserOutputSearch]:
        return Users.searchUsers(**locals())

    return router


def create_team_routes():
    router = APIRouter(prefix="/teams", tags=["Teams"])

    @router.post("/add")
    async def add_team(teamData: TeamInputAdd):
        return {"id": Users.addTeam(teamData)}

    @router.put("/update/{id}")
    async def update_team(id: int, teamData: TeamInputUpdate):
        return Users.updateTeam(id, teamData)

    @router.get("/search")
    async def search_teams(
        id: int | None = Query(None, ge=0),
        code: str | None = Query(None, max_length=50),
        leader: str | None = Query(None, max_length=50),
        limit: int = Query(10, gt=0),
        offset: int = Query(0, ge=0),
    ) -> list[TeamOutputSearch]:
        return Users.searchTeams(**locals())

    return router


def create_manager_routes():
    router = APIRouter(prefix="/managers", tags=["Managers"])

    @router.post("/add")
    async def add_manager(managerData: ManagerInputAdd):
        return {"id": Managers.add(managerData)}

    @router.put("/update/{id}")
    async def update_manager(id: int, managerData: ManagerInputUpdate):
        return Managers.update(id, managerData)

    @router.get("/search")
    async def search_managers(
        id: int | None = Query(None, ge=0),
        name: str | None = Query(None, max_length=50),
        role: str | None = None,
        limit: int = Query(10, gt=0),
        offset: int = Query(0, ge=0),
    ) -> list[Manager]:
        return Managers.search(**locals())

    return router


def create_task_routes():
    router = APIRouter(prefix="/tasks", tags=["Tasks"])

    @router.post("/add")
    async def add_task(taskData: TaskInputAdd):
        return {"id": Tasks.add(taskData)}

    @router.put("/update/{id}")
    async def update_task(id: int, taskData: TaskInputUpdate):
        return Tasks.update(id, taskData)

    @router.get("/search")
    async def search_tasks(
        id: int | None = Query(None, ge=0),
        name: str | None = Query(None, max_length=50),
        code: str | None = Query(None, max_length=50),
        hours_from: int | None = Query(None, ge=0),
        hours_to: int | None = Query(None, ge=0),
        limit: int = Query(10, gt=0),
        offset: int = Query(0, ge=0),
    ) -> list[TaskOutputSearch]:
        return Tasks.search(**locals())

    return router


def create_database_routes():
    router = APIRouter(tags=["Database"])

    @router.post("/populate_dummy_data")
    async def populate_dummy_data():
        """Populate the database with dummy data."""
        Users.addUserDummyData()
        Users.addTeamDummyData()
        Managers.addManagerDummyData()
        Tasks.addTaskDummyData()
        return {"status": "Dummy data populated successfully."}

    @router.post("/reset_database")
    async def reset_database():
        """Reset the database by truncating all data."""
        if os.path.exists("task_manager.db"):
            os.remove("task_manager.db")
        DB.init()
        return {"status": "Database reset successfully."}

    return router


# ========================= REGISTER ROUTERS =========================
app.include_router(create_user_routes())
app.include_router(create_team_routes())
app.include_router(create_manager_routes())
app.include_router(create_task_routes())
app.include_router(create_database_routes())
