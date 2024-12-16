import sqlite3

# helper class to work with database
class DB:

    @classmethod
    def init(cls):
        '''Create database and all the necessary tables'''
        with open('migrations/base.sql') as f:
            sql = f.read()
            sqlite3.connect(cls.dbFile(), isolation_level=None).executescript(sql)

    @classmethod
    def dbFile(cls):
        return 'task_manager.db'  # Changed to task_manager.db for task management system
    
    @classmethod
    def execute(cls, sql, params=()):
        '''Execute the sql query and return lastrowid'''
        with sqlite3.connect(cls.dbFile(), isolation_level=None) as conn:
            crs = conn.cursor()
            crs.execute(sql, params)
            return crs.lastrowid
    
    @classmethod
    def select(cls, sql, params=()) -> list:
        '''Select and return associated rows as a list of dictionaries'''
        with sqlite3.connect(cls.dbFile(), isolation_level=None) as conn:
            conn.row_factory = sqlite3.Row
            crs = conn.cursor()
            crs.execute(sql, params)
            return [dict(row) for row in crs.fetchall()] or []

    @classmethod
    def insert_user(cls, first_name: str, last_name: str, role: str, team_id: int | None = None):
        '''Insert a new user into the database'''
        sql = """
            INSERT INTO users (first_name, last_name, role, team_id)
            VALUES (?, ?, ?, ?)
        """
        return cls.execute(sql, (first_name, last_name, role, team_id))

    @classmethod
    def insert_team(cls, code: str, leader_id: int):
        '''Insert a new team into the database'''
        sql = """
            INSERT INTO teams (code, leader_id)
            VALUES (?, ?)
        """
        return cls.execute(sql, (code, leader_id))
    
    @classmethod
    def insert_task(cls, name: str, description: str, assigned_to: int, due_date: str, status: str):
        '''Insert a new task into the database'''
        sql = """
            INSERT INTO tasks (name, description, assigned_to, due_date, status)
            VALUES (?, ?, ?, ?, ?)
        """
        return cls.execute(sql, (name, description, assigned_to, due_date, status))
    
    @classmethod
    def select_users(cls, limit: int = 10, offset: int = 0) -> list:
        '''Select users from the database'''
        sql = """
            SELECT * FROM users
            LIMIT ? OFFSET ?
        """
        return cls.select(sql, (limit, offset))
    
    @classmethod
    def select_teams(cls, limit: int = 10, offset: int = 0) -> list:
        '''Select teams from the database'''
        sql = """
            SELECT * FROM teams
            LIMIT ? OFFSET ?
        """
        return cls.select(sql, (limit, offset))
    
    @classmethod
    def select_tasks(cls, limit: int = 10, offset: int = 0) -> list:
        '''Select tasks from the database'''
        sql = """
            SELECT * FROM tasks
            LIMIT ? OFFSET ?
        """
        return cls.select(sql, (limit, offset))
    
    @classmethod
    def select_user_by_id(cls, user_id: int) -> dict | None:
        '''Select user by id from the database'''
        sql = """
            SELECT * FROM users WHERE id = ?
        """
        result = cls.select(sql, (user_id,))
        return result[0] if result else None
    
    @classmethod
    def select_team_by_id(cls, team_id: int) -> dict | None:
        '''Select team by id from the database'''
        sql = """
            SELECT * FROM teams WHERE id = ?
        """
        result = cls.select(sql, (team_id,))
        return result[0] if result else None
    
    @classmethod
    def select_task_by_id(cls, task_id: int) -> dict | None:
        '''Select task by id from the database'''
        sql = """
            SELECT * FROM tasks WHERE id = ?
        """
        result = cls.select(sql, (task_id,))
        return result[0] if result else None
