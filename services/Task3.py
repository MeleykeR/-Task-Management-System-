from models.student import Student
from helpers.db import DB
from schemas.teacher_input_output import *

class Teachers:
    
    @classmethod
    def add(cls, teacherData: TeacherInputAdd) -> int:
        '''Add a teacher to the database and return the id of added item'''
        
        teacherId = DB.execute('''
                                INSERT INTO teachers (first_name, last_name, middle_name, gender, birth_date, academic_rank, scientific_degree)
                                values (?, ?, ?, ?, ?, ?, ?)''', 
                                (teacherData.first_name, teacherData.last_name, teacherData.middle_name, teacherData.gender, teacherData.birth_date, teacherData.academic_rank, teacherData.scientific_degree)
                            )
        
        return teacherId
    
    @classmethod
    def update(cls, id: int, teacherData: TeacherInputUpdate) -> Teacher:
        '''Update teacher by id, update only specified fields'''
        
        updateKeyValues = {field: value for field, value in teacherData.model_dump().items() if field in teacherData.model_fields_set and value is not None}
        
        if updateKeyValues:
            updateSql = 'UPDATE teachers SET ' + ', '.join([f'{key} = ?' for key in updateKeyValues.keys()]) + ', updated_at = CURRENT_TIMESTAMP WHERE id = ?'
            DB.execute(updateSql, (*updateKeyValues.values(), id))
        
        return cls.search(id=id)[0]  # Return the updated teacher
    
    @classmethod
    def search(
                cls, 
                id: int | None = None,
                name: str | None = None,
                academic_rank: AcademicRank | None = None,
                limit: int = 10,
                offset: int = 0
            ) -> list[Teacher]:
        '''Search teachers based on the provided filters'''
        
        sql = 'SELECT * FROM teachers '
        where, values = [], {}
        
        # Collect conditions for the WHERE clause
        if id is not None:
            where.append("id = :id")
            values['id'] = id
        
        if name is not None:
            where.append("(first_name LIKE :name OR last_name LIKE :name OR middle_name LIKE :name)")
            values['name'] = f'%{name}%'
        
        if academic_rank is not None:
            where.append("academic_rank = :academic_rank")
            values['academic_rank'] = academic_rank.value
        
        # Build the SQL query dynamically
        if where:
            sql += ' WHERE ' + ' AND '.join(where)
        
        # Add LIMIT and OFFSET
        sql += f' LIMIT {limit} OFFSET {offset}'
        
        # Execute and return the results
        return DB.select(sql, values)
    
    @classmethod
    def addTeacherDummyData(cls):
        '''Add dummy data for testing purposes'''
        DB.execute(f'''INSERT INTO teachers 
                    (id, first_name, last_name, middle_name, gender, birth_date, academic_rank, scientific_degree) VALUES 
                    (1, 'Samir', 'Ağayev', 'Vəli', 'male', '1986-08-03', '{AcademicRank.docent.value}', '{ScientificDegree.phd.value}'),
                    (2, 'Nigar', 'Əhmədova', 'Azər', 'female', '1990-01-02', '{AcademicRank.professor.value}', null)
                    ON CONFLICT DO NOTHING
                ''')
