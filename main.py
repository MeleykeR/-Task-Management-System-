import os

from fastapi import FastAPI, HTTPException, status, Query, Request, APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from contextlib import asynccontextmanager
from helpers.db import DB

from services.users import Users  # Renamed from 'students'
from services.managers import Managers  # Renamed from 'teachers'
from services.tasks import Tasks  # Renamed from 'subjects'

# Initialize database and create tables
@asynccontextmanager
async def lifespan(_: FastAPI):
    DB.init()
    yield

app = FastAPI(lifespan=lifespan, title='Task Management API', version='1.0', tags=['Task Management'])

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, e: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"name": type(e).__name__, "message": str(e)}
    )
    
# Redirect to /docs root path
@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def index():
    return "/docs"

#################### USERS ROUTES ####################

userRouter = APIRouter(prefix="/users", tags=["Users"])

from schemas.user_input_output import *  # Adapted schema for users

@userRouter.post("/add")
async def users_add(userData: UserInputAdd):
    return {'id': Users.addUser(userData=userData)}

@userRouter.put("/update/{id}")
async def users_update(id: int, userData: UserInputUpdate):
    return Users.updateUser(id=id, userData=userData)

@userRouter.get("/search")
async def users_search(
            id: int | None = Query(None, ge=0),
            name: str | None = Query(None, max_length=50),
            role: str | None = None,  # User role (e.g., 'developer', 'designer', etc.)
            limit: int | None = Query(10, gt=0),
            offset: int | None = Query(0, ge=0)
        ) -> list[UserOutputSearch]:
    return Users.searchUsers(**locals())

app.include_router(userRouter)

#################### TEAMS ROUTES ####################

teamRouter = APIRouter(prefix="/teams", tags=["Teams"])

from schemas.team_input_output import *  # Schema for teams

@teamRouter.post("/add")
async def teams_add(teamData: TeamInputAdd):
    return {'id': Users.addTeam(teamData=teamData)}

@teamRouter.put("/update/{id}")
async def teams_update(id: int, teamData: TeamInputUpdate):
    return Users.updateTeam(id=id, teamData=teamData)

@teamRouter.get("/search")
async def teams_search(
            id: int | None = Query(None, ge=0),
            code: str | None = Query(None, max_length=50),
            leader: str | None = Query(None, max_length=50),
            limit: int | None = Query(10, gt=0),
            offset: int | None = Query(0, ge=0),
        ) -> list[TeamOutputSearch]:
    return Users.searchTeams(**locals())

app.include_router(teamRouter)

#################### MANAGERS ROUTES ####################

managerRouter = APIRouter(prefix="/managers", tags=["Managers"])

from schemas.manager_input_output import *  # Schema for managers

@managerRouter.post("/add")
async def managers_add(managerData: ManagerInputAdd):
    return {'id': Managers.add(managerData=managerData)}

@managerRouter.put("/update/{id}")
async def managers_update(id: int, managerData: ManagerInputUpdate):
    return Managers.update(id=id, managerData=managerData)

@managerRouter.get("/search")
async def managers_search(
            id: int | None = Query(None, ge=0),
            name: str | None = Query(None, max_length=50),
            role: str | None = None,  # Manager role (e.g., 'project_manager')
            limit: int | None = Query(10, gt=0),
            offset: int | None = Query(0, ge=0)
        ) -> list[Manager]:
    return Managers.search(**locals())

app.include_router(managerRouter)

#################### TASKS ROUTES ####################

taskRouter = APIRouter(prefix="/tasks", tags=["Tasks"])

from schemas.task_input_output import *  # Schema for tasks

@taskRouter.post("/add")
async def tasks_add(taskData: TaskInputAdd):
    return {'id': Tasks.add(taskData=taskData)}

@taskRouter.put("/update/{id}")
async def tasks_update(id: int, taskData: TaskInputUpdate):
    return Tasks.update(id=id, taskData=taskData)

@taskRouter.get("/search")
async def tasks_search(
            id: int | None = Query(None, ge=0),
            name: str | None = Query(None, max_length=50),
            code: str | None = Query(None, max_length=50),
            hours_from: int | None = Query(None, ge=0),
            hours_to: int | None = Query(None, ge=0),
            limit: int | None = Query(10, gt=0),
            offset: int | None = Query(0, ge=0)
        ) -> list[TaskOutputSearch]:
    return Tasks.search(**locals())

app.include_router(taskRouter)

#################### DATABASE ROUTES ####################

dummyDataRouter = APIRouter(tags=["Database"])

@dummyDataRouter.post("/populate_dummy_data")
async def populate_dummy_data():
    '''Populate the database with dummy data'''
    
    Users.addUserDummyData()
    Users.addTeamDummyData()
    Managers.addManagerDummyData()
    Tasks.addTaskDummyData()
    
    return True

@dummyDataRouter.post("/reset_database")
async def reset_database():
    '''Reset the database and truncate all data'''
    
    os.remove('task_manager.db')
    DB.init()
    
    return True

app.include_router(dummyDataRouter)
