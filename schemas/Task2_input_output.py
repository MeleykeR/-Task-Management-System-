from pydantic import BaseModel
from schemas.user_input_output import UserOutputSearch  # This would be the equivalent to StudentOutputSearch for Users in your task system.

# Input model for adding a new team
class TeamInputAdd(BaseModel):
    code: str  # Unique code for the team
    leader_user_id: int | None = None  # Optional: User ID of the team leader (Starosta)

# Input model for updating an existing team
class TeamInputUpdate(BaseModel):
    code: str | None = None  # Optional: New team code
    leader_user_id: int | None = None  # Optional: New team leader (Starosta) user ID

# Output model to represent the team when searching or displaying it
class TeamOutputSearch(BaseModel):
    id: int
    code: str
    # Here we use UserOutputSearch to represent the leader 
    leader: UserOutputSearch | None = None  # This can be None if there's no assigned leader
