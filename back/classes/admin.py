from queries.admin_queries import *
from typing import Tuple , Any
from models.AdminModels import *
class Admin():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    @classmethod
    def _create_model_from_tuple (cls , row : Tuple[Any])-> UserList:
        return UserList(
            id = row[0],
            name = row[1],
            surname = row[2],
            email = row[3]
        )

    def get_user_list(
            self
    ):
        with self.db_conn as conn:
            results = conn.execute(GET_ALL_USERS_MAIL).fetchall()
        return [
            self._create_model_from_tuple(row)
            for row in results
        ]
    
    def user_view(
        self ,  
        user_id : int
    ):
        with self.db_conn as conn:
            result = conn.execute(USER_FULL_VIEW , (user_id, )).fetchone()
            if not result:
                return None
            columns = ["id" , "name" , "surname" , "profession" , "email" , "phone" , "avatar" , "age" , "experience" , "education" , "skills" , 'employment']
            user_dict = dict(zip(columns, result))
        return{"data" : user_dict}
    
    def user_data(
            self ,
            user_id : int
    ):  
        results_cols = ["article_interest" , "interested_at_article" , "ad_interest" , "interested_at_ad" , "article_comment" , "comment" , 'comment_at']
        result_cols=["connected_user" , "name" , "email" , "phone" ]
        res_cols = ["article_title" , "article" , "path_to_media" , "article_uploaded_at" , "ad_title" , "explanation" , "ad_uploaded_at" ]
        with self.db_conn as conn:
            res = conn.execute(USER_UPLOADS,(user_id,)).fetchall()
            result = conn.execute(USER_CONNECTIONS,(user_id,user_id,user_id)).fetchall()
            results = conn.execute(USER_INTERESTS_COMMENTS,(user_id,)).fetchall()

            uploads_data = [dict(zip(res_cols, upload)) for upload in res]

        # Organizing the connections data (e.g., connected users)
            connections_data = [dict(zip(result_cols, connection)) for connection in result]

            # Organizing the interests and comments data
            interests_comments_data = [dict(zip(results_cols, interest_comment)) for interest_comment in results]

            # Combine all results into one structured dictionary (or you could return them separately)
            combined_results = {
                "uploads": uploads_data,
                "connections": connections_data,
                "interests_comments": interests_comments_data
            }

            return combined_results
        
    def user_data_to_xml(self , user_data):
    # Initialize the XML content
        xml_content = "<user>\n"

        # Handling the uploads
        xml_content += "  <uploads>\n"
        for upload in user_data.get('uploads', []):
            xml_content += "    <item>\n"
            for key, value in upload.items():
                xml_content += f"      <{key}>{value}</{key}>\n"
            xml_content += "    </item>\n"
        xml_content += "  </uploads>\n"

        # Handling the connections
        xml_content += "  <connections>\n"
        for connection in user_data.get('connections', []):
            xml_content += "    <item>\n"
            for key, value in connection.items():
                xml_content += f"      <{key}>{value}</{key}>\n"
            xml_content += "    </item>\n"
        xml_content += "  </connections>\n"

        # Handling the interests and comments
        xml_content += "  <interests_comments>\n"
        for interest_comment in user_data.get('interests_comments', []):
            xml_content += "    <item>\n"
            for key, value in interest_comment.items():
                xml_content += f"      <{key}>{value}</{key}>\n"
            xml_content += "    </item>\n"
        xml_content += "  </interests_comments>\n"

        xml_content += "</user>"
        return xml_content
