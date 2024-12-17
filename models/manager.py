from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # Assuming you have a Base class in your database.py for SQLAlchemy

class Manager(Base):
    __tablename__ = 'managers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=True)
    
    # Define any relationships if needed, e.g., a manager can have many teams or tasks.
    teams = relationship("Team", backref="manager", lazy=True)  # Example of a one-to-many relationship
    
    def __repr__(self):
        return f"<Manager(id={self.id}, name={self.name}, role={self.role})>"

    # You can also add methods for convenience, such as for creating or updating manager details
    def update(self, name=None, email=None, role=None):
        if name:
            self.name = name
        if email:
            self.email = email
        if role:
            self.role = role
        # Return updated manager object if needed
        return self
