from models.student import Student
from models.student_group import StudentGroup
from helpers.db import DB

from schemas.student_input_output import *
from schemas.student_group_input_output import *

from fastapi import HTTPException, status

class Students:
    
    @classmethod
    def addStudent(cls, studentData: StudentInputAdd) -> int:
        '''Add a student to the database and return the id of the new student'''
        
        studentId = DB.execute('''INSERT INTO students 
                                  (first_name, last_name, middle_name, gender, birth_date, admission_year) 
                                  VALUES (?, ?, ?, ?, ?, ?)''', 
                                  (studentData.first_name, studentData.last_name, studentData.middle_name, 
                                   studentData.gender, studentData.birth_date, studentData.admission_year)
                             )        
        return studentId
    
    @classmethod
    def updateStudent(cls, id: int, studentData: StudentInputUpdate) -> Student:
        '''Update student by id, update only specified fields'''
        
        updateKeyValues = {field: value for field, value in studentData.model_dump().items() 
                           if field in studentData.model_fields_set and value is not None}
                
        if updateKeyValues:
            updateSql = 'UPDATE students SET ' + ', '.join([f'{key} = ?' for key in updateKeyValues.keys()]) + ', updated_at = CURRENT_TIMESTAMP WHERE id = ?'
            DB.execute(updateSql, (*updateKeyValues.values(), id))
            
        return cls.searchStudents(id=id)[0]
        
        
    @classmethod
    def searchStudents(
                cls, 
                id: int | None = None,
                name: str | None = None,
                gender: Gender | None = None,
                admission_year_from: int | None = None,
                admission_year_to: int | None = None,
                limit: int = 10,
                offset: int = 0
            ) -> list[Student]:
        '''Search students based on the provided filters'''
        
        sql = 'SELECT * FROM students '
        where, values = [], {}
        
        if id is not None:
            where.append("id = :id")
            values['id'] = id
            
        if name is not None:
            where.append("(first_name LIKE :name OR last_name LIKE :name OR middle_name LIKE :name)")
            values['name'] = f'%{name}%'
        
        if admission_year_from is not None:
            where.append("admission_year >= :admission_year_from")
            values['admission_year_from'] = admission_year_from
        
        if admission_year_to is not None:
            where.append("admission_year <= :admission_year_to")
            values['admission_year_to'] = admission_year_to
        
        sql += ' WHERE ' + ' AND '.join(where) if where else ''
        sql += f' LIMIT {limit} OFFSET {offset}'
        
        return DB.select(sql, values)
    
    
    @classmethod
    def addStudentGroup(cls, studentGroupData: StudentGroupInputAdd) -> int:
        '''Add a student group to the database and return the id of the new group'''
        
        if studentGroupData.starosta_student_id is not None:
            cls._validateStarosta(studentGroupData.starosta_student_id)
        
        return DB.execute('''INSERT INTO student_groups (code, starosta_student_id) 
                             VALUES (?, ?)''', 
                             (studentGroupData.code, studentGroupData.starosta_student_id)
                        )  
    
    @classmethod
    def updateStudentGroup(cls, id: int, studentGroupData: StudentGroupInputUpdate) -> StudentGroupOutputSearch:
        '''Update a student group and return the updated group'''
        
        if studentGroupData.starosta_student_id is not None:
            cls._validateStarosta(studentGroupData.starosta_student_id)
        
        updateKeyValues = {field: value for field, value in studentGroupData.model_dump().items() 
                           if field in studentGroupData.model_fields_set and value is not None}
        
        if updateKeyValues:
            updateSql = 'UPDATE student_groups SET ' + ', '.join([f'{key} = ?' for key in updateKeyValues.keys()]) + ', updated_at = CURRENT_TIMESTAMP WHERE id = ?'
            DB.execute(updateSql, (*updateKeyValues.values(), id))
            
        return cls.searchStudentGroups(id=id)[0]
    
    @classmethod
    def _validateStarosta(cls, starosta_student_id: int):
        '''Helper method to validate if the starosta student exists'''
        
        if not cls.searchStudents(id=starosta_student_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Student with id {starosta_student_id} does not exist')
    
    @classmethod
    def searchStudentGroups(
                cls, 
                id: int | None = None,
                code: str | None = None,
                starosta: str | None = None,
                limit: int = 10,
                offset: int = 0
            ) -> list[StudentGroupOutputSearch]:
        '''Search student groups based on the provided filters'''
        
        sql = '''SELECT sg.*, s.first_name AS starosta_first_name, s.last_name AS starosta_last_name
                 FROM student_groups sg
                 LEFT JOIN students s ON sg.starosta_student_id = s.id '''
        
        where, values = [], {}
        
        if id is not None:
            where.append("sg.id = :id")
            values['id'] = id
        
        if code is not None:
            where.append("sg.code LIKE :code")
            values['code'] = f'%{code}%'
        
        if starosta is not None:
            where.append("(s.first_name LIKE :starosta OR s.last_name LIKE :starosta)")
            values['starosta'] = f'%{starosta}%'
        
        sql += ' WHERE ' + ' AND '.join(where) if where else ''
        sql += f' LIMIT {limit} OFFSET {offset}'
        
        items = DB.select(sql, values)
        
        return items
    
    @classmethod
    def addStudentGroupDummyData(cls):
        DB.execute('''INSERT INTO student_groups (id, code, starosta_student_id) 
                      VALUES (1, '2000i', 1) 
                      ON CONFLICT DO NOTHING''')
