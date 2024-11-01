# ========================================ARTICLES==========================================
GET_ARTICLES_TITLES = """
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
LEFT JOIN connections c ON (ua.uploader_id = c.sender OR ua.uploader_id = c.receiver)
LEFT JOIN article_categories ac ON ua.category_id = ac.id
WHERE (c.sender = ? OR c.receiver = ? AND c.state = 'Accepted') OR ua.uploader_id = ?
ORDER BY ua.uploaded_at DESC
"""

GET_INTEREST_ARTICLES = """
SELECT DISTINCT 
    u.id AS user_id, 
    u.name, 
    u.surname,  
    ua.id AS article_id, 
    ua.title, 
    ua.uploader_id, 
    ai.user_id,
    ac.category_name
FROM users u
JOIN uploaded_articles ua ON u.id = ua.uploader_id 
JOIN article_interest ai ON ua.id = ai.article_id
JOIN connections c ON (ai.user_id = c.sender OR ai.user_id = c.receiver)
LEFT JOIN article_categories ac ON ua.category_id = ac.id
WHERE (c.sender = ? OR c.receiver = ?) 
AND c.state = 'Accepted' 
AND (ai.user_id != ? AND ua.uploader_id != ?)
"""

GET_USER_INTEREST = """
SELECT article_id 
FROM article_interest 
WHERE user_id = ?
"""
GET_FULL_ARTICLE="""
SELECT article , path_to_media
FROM uploaded_articles
WHERE id = ?
 """
UPLOAD_ARTICLE = """
INSERT INTO uploaded_articles(id , uploader_id , title , article , category_id  , uploaded_at)
VALUES (NULL , ? , ? , ?,? , ?)
"""
UPLOAD_ARTICLE_MEDIA = """
UPDATE uploaded_articles
SET path_to_media = ?
WHERE id = ? 
"""
POST_ARTICLE_INTEREST = """
INSERT INTO article_interest
VALUES (NULL , ? , ? , ?)
"""
DELETE_ARTICLE_INTEREST="""
DELETE FROM article_interest
WHERE article_id = ? AND user_id = ?
"""

GET_LAST_INSERT =   """
SELECT last_insert_rowid() 
"""

COMMENT_ARTICLE="""
INSERT INTO article_comments
VALUES (NULL , ? , ? , ? , ?)
"""

GET_MY_ARTICLES= """
SELECT id , title
FROM uploaded_articles
WHERE uploader_id = ?
"""
UPDATE_ARTICLE ="""
UPDATE uploaded_articles 
SET title = ? , article = ? , category_id = ?
WHERE id = ?
"""


