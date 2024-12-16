from helpers.db import DB
from schemas.subject_input_output import *
from models.subject import Subject

class Subjects:
    
    @classmethod
    def add(cls, inputData: SubjectInputAdd) -> int:
        '''Add a subject to the database and return the id of added item'''
        
        fields = ', '.join(inputData.model_dump().keys())
        values = ', '.join(['?']*len(inputData.model_dump().keys()))
        sql = f'INSERT INTO subjects ({fields}) values ({values})'
        
        subject_id = DB.execute(sql, tuple(inputData.model_dump().values()))
        return subject_id
    
    @classmethod
    def update(cls, id: int, inputData: SubjectInputUpdate) -> Subject:
        '''Update subject by id, update only specified fields'''
        
        # Gather updated fields
        updateKeyValues = {field: value for field, value in inputData.model_dump().items() if field in inputData.model_fields_set and value is not None}
        
        if updateKeyValues:
            updateSql = 'UPDATE subjects SET ' + ', '.join([f'{key} = ?' for key in updateKeyValues.keys()]) + ', updated_at = CURRENT_TIMESTAMP WHERE id = ?'
            DB.execute(updateSql, (*updateKeyValues.values(), id))
            
        return cls.search(id=id)[0]  # Return the updated subject
    
    @classmethod
    def search(
                cls, 
                id: int | None = None,
                name: str | None = None,
                code: str | None = None,
                hours_from: int | None = None,
                hours_to: int | None = None,
                limit: int = 10,
                offset: int = 0
            ) -> list[SubjectOutputSearch]:
        '''Search subjects based on the provided filters'''
        
        sql = 'SELECT * FROM subjects '
        where, values = [], {}
        
        # Collect conditions for the WHERE clause
        if id is not None:
            where.append("id = :id")
            values['id'] = id
        
        if code is not None:
            where.append("code = :code")
            values['code'] = code
            
        if name is not None:
            where.append("(name LIKE :name OR code LIKE :name)")
            values['name'] = f'%{name}%'
        
        if hours_from is not None:
            where.append("hours >= :hours_from")
            values['hours_from'] = hours_from
        
        if hours_to is not None:
            where.append("hours <= :hours_to")
            values['hours_to'] = hours_to
        
        # Build the SQL query dynamically
        if where:
            sql += ' WHERE ' + ' AND '.join(where)
        
        # Add LIMIT and OFFSET
        sql += f' LIMIT {limit} OFFSET {offset}'
        
        # Execute and return the results
        return DB.select(sql, values)
    
    @classmethod
    def addSubjectDummyData(cls):
        '''Add dummy data for testing purposes'''
        DB.execute('''INSERT INTO subjects (id, name, code, hours, credits) VALUES 
                      (1, 'Object Oriented Programming', 'OOP', 60, 5),
                      (2, 'Programming Basics - 2', 'PB2', 45, NULL)
                      ON CONFLICT DO NOTHING
                   ''')
