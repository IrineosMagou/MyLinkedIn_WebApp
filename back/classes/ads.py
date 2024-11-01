from models.AdsModels import *
from typing import Tuple , Any , List , Union , Optional
from queries.ads_queries import *
from datetime import datetime

class Ads():
    def __init__(self , db_conn):
        self.db_conn = db_conn

    @classmethod
    def _create_model_from_tuple (cls , row : Tuple[Any])-> Union[AdResponse, FriendInterestAd]:
        row_length = len(row)
        if row_length == 6 :
            return AdResponse(
                id = row[0] ,
                name = row[1] ,
                surname = row[2] ,
                ad_id = row [3] , 
                title = row[4] ,
                uploader = row[5]
            )
        
        elif row_length == 7:
            return FriendInterestAd(
                id=row[0],
                name=row[1],
                surname=row[2],
                ad_id = row [3] , 
                title = row[4] ,
                uploader = row[5],
                friend_id=row[6]
             )
        else:
            raise ValueError("Invalid row length")

    def user_ads(
            self, 
            id: int
    ):
        with self.db_conn as conn:   
            result = conn.execute(GET_ADS_TITLES, (id, id, id)).fetchall()
            res = conn.execute(GET_INTEREST_ADS, (id, id, id , id)).fetchall()
            res1 = conn.execute(GET_USER_INTEREST, (id,)).fetchall()

            # Handle the case where res1 is None
            if res1 is None: 
                user_interested_ads_ids = set()
            else:
                user_interested_ads_ids = {row[0] for row in res1}  # Assume art_id is in the first position
            if not (result or res):
                return None

            combined_results = {
                'AdTitle': [],
                'InterestAd': []
            }

            # Process and categorize the articles
            for row in result:
                model_data = self._create_model_from_tuple(row)

                # Set the `isInterest` flag based on whether `art_id` is in user's interested articles
                model_data.isInterest = row[4] in user_interested_ads_ids

                combined_results['AdTitle'].append(model_data)  # Append model data after setting interest

            for row in res:
                model_data = self._create_model_from_tuple(row)

                # Set the `isInterest` flag based on whether `art_id` is in user's interested articles
                model_data.isInterest = row[4] in user_interested_ads_ids

                combined_results["InterestAd"].append(model_data)  # Append model data after setting interest
        return combined_results

    def full_ad(#only sending the full article.frontend has the rest info
            self ,
            ad_id : int
    ):
        with self.db_conn as conn:
            result = conn.execute(GET_FULL_AD , (ad_id, )).fetchone()
            if not result:
                # print(f"This is the ad id : {ad_id}")
                return None
            return FullAdResponse(
                ad = result[0] ,
            )

    def upload_ads(
            self ,
            user_id : int ,
            ad : UploadAd
    ):
        ts = datetime.utcnow()
        with self.db_conn as conn:
            if ad.id:
                conn.execute(UPDATE_AD ,(ad.title , ad.text , ad.id))
            else:
                conn.execute(UPLOAD_AD , (user_id, ad.title , ad.text , ts))
        return "Επιτυχής Ανέβασμα"
            

    def ad_interest(
            self ,
            id : int ,
            ad_id : int ,
            interest : bool
    ):
        ts = datetime.utcnow()
        with self.db_conn as conn:
            if interest == True:
                conn.execute(POST_AD_INTEREST , ( ad_id , id , ts))
                return{"Message " : "Επιτυχής Δήλωση Ενδιαφέρον"}
            else:
                conn.execute(DELETE_AD_INTEREST,(ad_id , id))
                return{"Message " : "Επιτυχής διαγραφή Ενδιαφέρον"}
    
    def article_comment(
            self ,
            id : int ,
            ad_id : int ,
            comment : str
    ):
        ts = datetime.utcnow()
        with self.db_conn as conn:
            conn.execute(COMMENT_ARTICLE , (id , ad_id , comment , ts))
            return "Επιτυχής σχόλιο"


    def my_ads(
            self,
            user_id: int
    ):
        with self.db_conn as conn:
            res = conn.execute(GET_MY_ADS,(user_id ,)).fetchall()
            if not res:
                return None
            columns = ["id" , "title"]
            article_dict = [dict(zip(columns, row)) for row in res]
            return article_dict