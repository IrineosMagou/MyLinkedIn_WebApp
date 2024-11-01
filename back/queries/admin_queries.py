GET_ALL_USERS_MAIL = """
SELECT id , name , surname , email
FROM users
WHERE is_admin = 0 ;
"""

USER_FULL_VIEW = """
SELECT u.id , u.name , u.surname , p.profession , u.email, u.phone, up.PathToPic , p.age , p.experience , p.education , p.skills , p.employment_agency
FROM users u
JOIN personal_info p ON u.id = p.user_id 
JOIN user_picture up ON u.id = up.user_pic
WHERE u.id = ?
"""

USER_UPLOADS = """
SELECT 
    u.title AS article_title, 
    u.article, 
    u.path_to_media, 
    u.uploaded_at AS article_uploaded_at,
    ua.title AS ad_title, 
    ua.explanation, 
    ua.uploaded_at AS ad_uploaded_at
FROM 
    uploaded_articles u
JOIN 
    uploaded_ads ua 
    ON u.uploader_id = ua.uploader_id
WHERE 
    u.uploader_id = ?;
"""
USER_INTERESTS_COMMENTS = """
SELECT
    a.article_id AS article_id, 
    a.interest_at , ai.ad_id ,
    ai.interest_at , 
    ac.article_id AS article_comment , ac.comment , ac.comment_at
FROM article_interest a 
JOIN ad_interest ai ON a.user_id = ai.user_id
JOIN article_comments ac ON a.user_id = ac.user_id 
WHERE a.user_id = ?
"""
USER_CONNECTIONS = """
SELECT DISTINCT u.id, u.name, u.email, u.phone
FROM connections c
JOIN users u ON (c.receiver = u.id OR c.sender = u.id)
WHERE (c.sender = ? OR c.receiver = ?) AND u.id != ?
"""

