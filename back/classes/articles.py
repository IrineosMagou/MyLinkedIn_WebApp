from models.ArticleModels import *
from typing import Tuple , Any , List , Union , Optional
from fastapi import UploadFile ,  HTTPException
from queries.article_queries import *
from recommendations.system import get_recommendations_for_user
import shutil
from datetime import datetime
import uuid
import os

BASE_MEDIA_DIR = "/path/to/media/"
MEDIA_PATH = 'media/'

class Articles():
    def __init__(self , db_conn):
        self.db_conn = db_conn

    @classmethod
    def _create_model_from_tuple (cls , row : Tuple[Any])-> Union[ArticleResponse, FriendInterestArticle]:
        row_length = len(row)
        if row_length == 7:
            return ArticleResponse(
                id = row[0] ,
                name = row[1] ,
                surname = row[2] ,
                art_id = row [3] , 
                title = row[4] ,
                uploader = row[5],
                category_name = row[6]
            )
        
        elif row_length == 8:
            return FriendInterestArticle(
                id=row[0],
                name=row[1],
                surname=row[2],
                art_id = row [3] , 
                title = row[4] ,
                uploader = row[5],
                friend_id=row[6],
                category_name = row[7]

             )
        else:
            raise ValueError("Invalid row length")

    def user_articles(
            self, 
            id: int
    ):
        with self.db_conn as conn:   
            result = conn.execute(GET_ARTICLES_TITLES, (id, id, id)).fetchall()
            res = conn.execute(GET_INTEREST_ARTICLES, (id, id, id , id)).fetchall()
            res1 = conn.execute(GET_USER_INTEREST, (id,)).fetchall()
            rec = get_recommendations_for_user(id , 6)
            article_ids_list = rec.tolist() 
            ids_string = ','.join(map(str, article_ids_list)) 
            query = f"""
            SELECT DISTINCT 
                u.id AS user_id, 
                u.name, 
                u.surname,  
                ua.id AS article_id, 
                ua.title, 
                ua.uploader_id,
                ac.category_name
            FROM uploaded_articles ua
            JOIN users u ON ua.uploader_id = u.id
            LEFT JOIN article_categories ac ON ua.category_id = ac.id
            WHERE ua.id IN ({ids_string})
            """
            # Execute the query
            articles_rec = conn.execute(query).fetchall()
            if res1 is None: 
                user_interested_art_ids = set()
            else:
                user_interested_art_ids = {row[0] for row in res1}  
            combined_results = {
                'ArticleTitle': [],
                'InterestArticle': [],
                'Recommended' : []
            }
            if not (result or res):
                for row in articles_rec:
                    model_data = self._create_model_from_tuple(row)
                    # Set the `isInterest` flag based on whether `art_id` is in user's interested articles
                    model_data.isInterest = row[4] in user_interested_art_ids
                    combined_results["Recommended"].append(model_data)
                return combined_results

            # Process and categorize the articles
            for row in result:
                model_data = self._create_model_from_tuple(row)
                
                model_data.isInterest = row[4] in user_interested_art_ids
                combined_results['ArticleTitle'].append(model_data)  
            for row in res:
                model_data = self._create_model_from_tuple(row)
                
                model_data.isInterest = row[4] in user_interested_art_ids
                combined_results["InterestArticle"].append(model_data)  
            for row in articles_rec:
                model_data = self._create_model_from_tuple(row)
                
                model_data.isInterest = row[4] in user_interested_art_ids
                combined_results["Recommended"].append(model_data)
        return combined_results


    def full_article(#only sending the full article.frontend has the rest info
            self ,
            art_id : int
    ):
        with self.db_conn as conn:
            result = conn.execute(GET_FULL_ARTICLE , (art_id, )).fetchone()
            if not result:
                # print(f"THis is the article id : {art_id}")
                return None
            elif not result[1]:
                return result[0]
            try:
                 files = os.listdir(result[1])
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="Media directory not found")
            return [
                 FullArticleResponse(
                article = result[0] ,
                media = files
            )]

    def upload_articles(
            self ,
            user_id : int ,
            title : str , 
            article : str ,
            category : Optional[int] = None,
            art_id : Optional[int] = None,
            media: Optional[List[UploadFile]] = None
    ):
        ts = datetime.utcnow()
        with self.db_conn as conn:
            if art_id:
                cat_id = conn.execute("SELECT id FROM article_categories WHERE category_name = ?" , (category ,)).fetchone()
                # print(type(title), type(article), type(cat_id), type(art_id)) 
                conn.execute(UPDATE_ARTICLE , ( title , article , cat_id[0] ,  art_id ))
            else:
                cat_id = conn.execute("SELECT id FROM article_categories WHERE category_name = ?" , (category ,)).fetchone()
                conn.execute(UPLOAD_ARTICLE , (user_id, title , article ,cat_id[0], ts))
            res = conn.execute(GET_LAST_INSERT).fetchone()
            dir_name = 'article' + str(res[0])
            if media:
                article_dir = os.path.join(BASE_MEDIA_DIR, dir_name)
                if os.path.exists(article_dir):
                    shutil.rmtree(article_dir)
                os.makedirs(article_dir)
                for md in media:
                    id_media = uuid.uuid4().hex[:10]  # Unique ID for each media file
                    file_extension = md.filename.split('.')[-1]
                    media_name = f"{id_media}.{file_extension}"
                    pic_path = os.path.join(article_dir, media_name)
                    with open(pic_path, "wb") as writer:
                        writer.write(md.file.read())
                    path_to_save = os.path.join(MEDIA_PATH, dir_name)
                    conn.execute(UPLOAD_ARTICLE_MEDIA, (path_to_save, res[0]))
        return{"Message " : "Επιτυχής ανέβασμα"}
    
    def article_interest(
            self ,
            id : int ,
            article_id : int ,
            interest : bool
    ):
        ts = datetime.utcnow()
        with self.db_conn as conn:
            if interest == True:
                conn.execute(POST_ARTICLE_INTEREST , ( article_id , id , ts))
                return{"Message " : "Επιτυχής Δήλωση Ενδιαφέρον"}
            else:
                conn.execute(DELETE_ARTICLE_INTEREST,(article_id , id))
                return{"Message " : "Επιτυχής διαγραφή Ενδιαφέρον"}
    
    def article_comment(
            self ,
            id : int ,
            article_id : int ,
            comment : str
    ):
        ts = datetime.utcnow()
        with self.db_conn as conn:
            conn.execute(COMMENT_ARTICLE , (id , article_id , comment , ts))
            return "Επιτυχής σχόλιο"

    def my_articles(
            self,
            user_id: int
    ):
        with self.db_conn as conn:
            res = conn.execute(GET_MY_ARTICLES,(user_id ,)).fetchall()
            if not res:
                return None
            columns = ["id" , "title"]
            article_dict = [dict(zip(columns, row)) for row in res]
            return article_dict
    
    
