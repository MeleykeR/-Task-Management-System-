from typing import List
from sqlalchemy.orm import Session
from models import Manager  # Assuming you have a Manager model defined in models.py
from schemas.manager_input_output import ManagerInputAdd, ManagerInputUpdate, ManagerOutputSearch
from helpers.db import DB  # Assuming DB is a utility that provides the database connection/session


class Managers:
    @staticmethod
    def add(managerData: ManagerInputAdd) -> int:
        """Add a new manager to the database."""
        db: Session = DB.get_session()
        new_manager = Manager(
            name=managerData.name,
            email=managerData.email,
            role=managerData.role,
            # other fields as per your model and schema
        )
        db.add(new_manager)
        db.commit()
        db.refresh(new_manager)
        db.close()
        return new_manager.id  # Assuming Manager has an 'id' field

    @staticmethod
    def update(id: int, managerData: ManagerInputUpdate) -> bool:
        """Update an existing manager's details."""
        db: Session = DB.get_session()
        manager = db.query(Manager).filter(Manager.id == id).first()
        
        if not manager:
            db.close()
            return False

        manager.name = managerData.name
        manager.email = managerData.email
        manager.role = managerData.role
        # Update other fields as necessary
        
        db.commit()
        db.close()
        return True

    @staticmethod
    def search(name: str | None = None, role: str | None = None, limit: int = 10, offset: int = 0) -> List[ManagerOutputSearch]:
        """Search for managers based on given parameters."""
        db: Session = DB.get_session()
        
        query = db.query(Manager)
        
        if name:
            query = query.filter(Manager.name.ilike(f"%{name}%"))
        if role:
            query = query.filter(Manager.role == role)
        
        managers = query.offset(offset).limit(limit).all()
        db.close()
        
        # Convert managers to the output schema
        return [ManagerOutputSearch(id=manager.id, name=manager.name, email=manager.email, role=manager.role) for manager in managers]


    @staticmethod
    def add_manager_dummy_data():
        """Add dummy manager data."""
        db: Session = DB.get_session()
        
        dummy_managers = [
            Manager(name="John Doe", email="john.doe@example.com", role="project_manager"),
            Manager(name="Jane Smith", email="jane.smith@example.com", role="team_lead")
            # Add more dummy data as needed
        ]
        
        db.bulk_save_objects(dummy_managers)
        db.commit()
        db.close()
