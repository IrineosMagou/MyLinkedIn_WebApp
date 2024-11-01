from models.models_user import Personal_Info
from typing import Tuple , Any , Dict
from queries.user_queries import INSERT_PERSONAL_INFO , CHECK_FOR_PERSONAL_INFO , GET_PERSONAL_INFO

class PersonalInfo():
    def __init__(self, db_conn):
        self.db_conn = db_conn
    
    def info_management(
            self ,
            id : int , 
            info : Personal_Info

    ):
        # print(f'This is personal_info {id}')
        with self.db_conn as conn :
            res = conn.execute(CHECK_FOR_PERSONAL_INFO ,(id ,)).fetchone()
            if res :
                updates = {}
                if info.age is not None:
                    updates['age'] = info.age
                    updates['is_age_p'] = info.is_age_p  # Add privacy flag for 'age'

                if info.experience is not None:
                    updates['experience'] = info.experience
                    updates['is_experience_p'] = info.is_experience_p  # Add privacy flag for 'experience'

                if info.education is not None:
                    updates['education'] = info.education
                    updates['is_education_p'] = info.is_education_p  # Add privacy flag for 'education'

                if info.skills is not None:
                    updates['skills'] = info.skills
                    updates['is_skills_p'] = info.is_skills_p  # Add privacy flag for 'skills'

                if info.employment is not None:
                    updates['employment_agency'] = info.employment
                    updates['is_employment_agency_p'] = info.is_employment_p
                success = self.update_personal_info(id, updates)
                if success:
                    return 1
            conn.execute(INSERT_PERSONAL_INFO,(id ,info.profession , info.age ,  info.experience , info.education , info.skills , 
                                               info.employment ,info.is_age_p ,info.is_experience_p ,info.is_education_p , info.is_skills_p , info.is_employment_p))
            return 1
    
    def update_personal_info(
                self, 
                user_id: int,
                updates: Dict[str, any]
    ):
        # Prepare the base SQL query
        base_query = "UPDATE personal_info SET "
        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        query = base_query + set_clause + " WHERE user_id = ?"
        values = list(updates.values()) + [user_id]
        with self.db_conn as conn :
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
        return 1
    
    def personal_info_view(
            self,
            user_id : int
    ):
        with self.db_conn as conn:
            res = conn.execute( GET_PERSONAL_INFO,(user_id ,)).fetchone()
            return res

        
