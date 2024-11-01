
GET_ADS_TITLES = """
SELECT DISTINCT u.id, u.name, u.surname, ua.id , ua.title, ua.uploader_id
FROM uploaded_ads ua
JOIN users u ON ua.uploader_id = u.id
LEFT JOIN connections c ON (ua.uploader_id = c.sender OR ua.uploader_id = c.receiver)
WHERE (c.sender = ? OR c.receiver = ? AND c.state = 'Accepted') OR ua.uploader_id = ?
ORDER BY ua.uploaded_at DESC
"""
GET_INTEREST_ADS = """
SELECT DISTINCT u.id, u.name, u.surname, ua.id , ua.title, ua.uploader_id , ai.user_id
FROM users u
JOIN uploaded_ads ua ON u.id = ua.uploader_id 
JOIN ad_interest ai ON ua.id = ai.ad_id
JOIN connections c ON (ai.user_id = c.sender OR ai.user_id = c.receiver)
WHERE (c.sender = ? OR c.receiver = ?) 
AND c.state = 'Accepted' 
AND (ai.user_id != ? AND ua.uploader_id !=?)
"""
GET_USER_INTEREST = """
SELECT ad_id
FROM ad_interest 
WHERE user_id = ?
"""
GET_FULL_AD="""
SELECT explanation
FROM uploaded_ads
WHERE id = ?
 """

UPLOAD_AD = """
INSERT INTO uploaded_ads
VALUES (NULL , ? , ? , ? , ?)
"""

POST_AD_INTEREST = """
INSERT INTO ad_interest
VALUES (NULL , ? , ? , ?)
"""
DELETE_AD_INTEREST="""
DELETE FROM ad_interest
WHERE ad_id = ? AND user_id = ?
"""

GET_LAST_INSERT =   """
SELECT last_insert_rowid() 
"""

COMMENT_ARTICLE="""
INSERT INTO article_comments
VALUES (NULL , ? , ? , ? , ?)
"""

GET_MY_ADS= """
SELECT id , title
FROM uploaded_ads
WHERE uploader_id = ?
"""
UPDATE_AD ="""
UPDATE uploaded_ads 
SET title = ? , explanation  = ?
WHERE id = ?
"""