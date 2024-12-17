from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace 'sqlite:///example.db' with your database URL (e.g., PostgreSQL, MySQL)
DATABASE_URL = "sqlite:///example.db"

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for defining database models
Base = declarative_base()

# Example database table (Model)
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)

# Create the database tables (run this once to initialize the database)
def init_db():
    Base.metadata.create_all(bind=engine)

# Dependency for getting a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
3. How It Works
Database Connection

The create_engine function establishes a connection to the database.
sqlite:///example.db is used for SQLite, but you can replace it with PostgreSQL or MySQL connection strings.
Model Definition

The Task class defines a table with columns id, title, and description.
Session Management

SessionLocal manages sessions to interact with the database.
get_db is used as a dependency to provide a database session in your FastAPI routes.
Initialization

init_db() creates the necessary tables in the database.
4. Using database.py in Your FastAPI App
Update main.py to include the database logic:

python
Copy code
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import init_db, get_db, Task

# Initialize the database
init_db()

app = FastAPI()

# Create a task (example route)
@app.post("/tasks/")
def create_task(title: str, description: str, db: Session = Depends(get_db)):
    new_task = Task(title=title, description=description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"task": {"id": new_task.id, "title": new_task.title, "description": new_task.description}}

# Read all tasks
@app.get("/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return {"tasks": tasks}
