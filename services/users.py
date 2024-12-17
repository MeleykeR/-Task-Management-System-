from helpers.db import DB
from schemas.user_input_output import UserInputAdd, UserInputUpdate, UserOutputSearch


class Users:
    @staticmethod
    def addUser(userData: UserInputAdd) -> int:
        """
        Add a new user to the database.
        :param userData: UserInputAdd schema
        :return: ID of the newly created user
        """
        query = """
        INSERT INTO users (name, role, email)
        VALUES (?, ?, ?)
        """
        params = (userData.name, userData.role, userData.email)
        return DB.execute(query, params, commit=True)

    @staticmethod
    def updateUser(id: int, userData: UserInputUpdate) -> dict:
        """
        Update an existing user in the database.
        :param id: ID of the user to update
        :param userData: UserInputUpdate schema
        :return: Success message
        """
        query = """
        UPDATE users
        SET name = ?, role = ?, email = ?
        WHERE id = ?
        """
        params = (userData.name, userData.role, userData.email, id)
        DB.execute(query, params, commit=True)
        return {"message": f"User with ID {id} has been updated successfully"}

    @staticmethod
    def searchUsers(
        id: int = None,
        name: str = None,
        role: str = None,
        limit: int = 10,
        offset: int = 0
    ) -> list[UserOutputSearch]:
        """
        Search users in the database with optional filters.
        :param id: User ID
        :param name: User name
        :param role: User role
        :param limit: Number of records to return
        :param offset: Starting point for records
        :return: List of UserOutputSearch schema
        """
        query = "SELECT id, name, role, email FROM users WHERE 1=1"
        params = []

        if id is not None:
            query += " AND id = ?"
            params.append(id)
        if name is not None:
            query += " AND name LIKE ?"
            params.append(f"%{name}%")
        if role is not None:
            query += " AND role = ?"
            params.append(role)

        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = DB.fetch(query, tuple(params))
        return [UserOutputSearch(id=row[0], name=row[1], role=row[2], email=row[3]) for row in rows]

    @staticmethod
    def addUserDummyData():
        """
        Populate the users table with dummy data.
        """
        dummy_users = [
            ("John Doe", "developer", "john@example.com"),
            ("Jane Smith", "designer", "jane@example.com"),
            ("Bob Johnson", "manager", "bob@example.com"),
        ]

        query = "INSERT INTO users (name, role, email) VALUES (?, ?, ?)"
        for user in dummy_users:
            DB.execute(query, user, commit=True)

    @staticmethod
    def addTeam(teamData):
        """
        Placeholder for adding a team (if related to users).
        """
        raise NotImplementedError("Team handling not implemented in this file.")

    @staticmethod
    def updateTeam(id, teamData):
        """
        Placeholder for updating a team.
        """
        raise NotImplementedError("Team handling not implemented in this file.")

    @staticmethod
    def searchTeams(**kwargs):
        """
        Placeholder for searching teams.
        """
        raise NotImplementedError("Team handling not implemented in this file.")
