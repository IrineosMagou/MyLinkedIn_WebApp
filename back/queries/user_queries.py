
# =================================CREATION-AND-SIGN-IN===========================
CHECK_NEW_EMAIL_QUERY = """ 
SELECT * FROM users 
WHERE email = ?
"""
CREATE_USER_QUERY = """
INSERT INTO users
VALUES(NULL , ? , ? , ? , ? , ? , ?  )
"""
GET_LAST_INSERT =   """
SELECT last_insert_rowid() 
"""
SIGN_IN_CHECK_QUERY = """ 
SELECT  email , password_hash , id  , is_admin
FROM users
WHERE email = ? 
"""
INSERT_PICTURES_QUERY = """
INSERT INTO user_picture
VALUES (NULL,? , ?)
"""
AUTHORIZE_TOKEN_QUERY = """ 
SELECT id  FROM users 
WHERE id = ?
"""

# ==================================USER_VIEW=========================================
CONNECTED_USER_FULL_VIEW = """
SELECT u.id , u.name , u.surname , p.profession , u.email, u.phone, up.PathToPic , p.age , p.experience , p.education , p.skills
FROM users u
JOIN personal_info p ON u.id = p.user_id 
JOIN user_picture up ON u.id = up.user_pic
WHERE u.id = ?
"""

NOT_CONNECTED_USER_FULL_VIEW = """
SELECT 
    u.id,
    u.name,
    u.surname,
    pi.profession,
    u.email,
    u.phone,
    p.PathToPic,
    CASE WHEN pi.is_age_p = false THEN pi.age ELSE NULL END AS age,
    CASE WHEN pi.is_experience_p = false THEN pi.experience ELSE NULL END AS experience,
    CASE WHEN pi.is_education_p = false THEN pi.education ELSE NULL END AS education,
    CASE WHEN pi.is_skills_p = false THEN pi.skills ELSE NULL END AS skills
FROM users u
JOIN user_picture p ON u.id = p.user_pic
LEFT JOIN personal_info pi ON u.id = pi.user_id
WHERE u.id = ?
"""
CONNECTION_PENDING = """
SELECT sender
FROM connections
WHERE ((sender = ? and receiver = ?) or (sender = ? and receiver = ?)) and state = "Pending"
"""
IS_USER_CONNECTED = """
SELECT *
FROM connections
WHERE ((sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)) AND state = "Accepted"
"""

GET_CONNECTION_STATUS = """
SELECT state , sender
FROM connections
WHERE (sender = ? and receiver = ?) or (sender = ? and receiver = ?)
"""


# ========================================NOTIFICATIONS=====================================
PENDING_CONNECTIONS = """
SELECT u.id , u.name , u.email, u.phone, p.PathToPic  
FROM users u
JOIN user_picture p ON u.id = p.user_pic
JOIN connections c ON u.id = c.sender
WHERE  (c.receiver = ? and c.state = "Pending")
"""

ARTICLES_INTERACT = """
SELECT 
    ua.id AS article_id, 
    ua.title, 
    u.id AS user_id,
    u.name,
    u.surname,
    ua.uploader_id ,
    'interest' AS interaction_type,
    ai.interest_at AS interaction_time
FROM uploaded_articles ua
JOIN article_interest ai ON ua.id = ai.article_id
JOIN users u ON ai.user_id = u.id
WHERE ua.uploader_id = ?

UNION

SELECT 
    ua.id AS article_id, 
    ua.title, 
    u.id AS user_id,
    u.name,
    u.surname,
    ua.uploader_id ,
    'comment' AS interaction_type,
    ac.comment_at AS interaction_time
FROM uploaded_articles ua
JOIN article_comments ac ON ua.id = ac.article_id
JOIN users u ON ac.user_id = u.id
WHERE ua.uploader_id = ?;

"""
# ========================================CONNECTIONS=======================================
SEARCH_USERS = """
SELECT 
    u.id,
    u.name,
    u.email,
    u.phone,
    p.PathToPic
FROM users u
JOIN user_picture p ON u.id = p.user_pic
LEFT JOIN personal_info pi ON u.id = pi.user_id
WHERE pi.profession = ? AND u.id != ?

"""
NEW_CONNECTION = """
INSERT INTO connections
VALUES(NULL , ? , ? , "Pending" , ? , NULL , NULL)
"""
GET_CONNECTIONS = """
SELECT DISTINCT u.id, u.name, u.email, u.phone, u0.PathToPic
FROM connections c
JOIN users u ON (c.receiver = u.id OR c.sender = u.id)
JOIN user_picture u0 ON u.id = u0.user_pic
WHERE (c.sender = ? OR c.receiver = ?) AND u.id != ? AND state = 'Accepted'
"""

#REQUESTS   
ACCEPT_REQUEST = """
UPDATE connections 
SET state = "Accepted" , accepted_at = ? 
WHERE (sender = ? and receiver = ? )
"""
DECLINE_REQUEST = """
UPDATE connections 
SET state =  "Rejected" , rejected_at = ? 
WHERE (sender = ? and receiver = ? )
"""
CANCEL_REQUEST = """
DELETE FROM connections 
WHERE ( receiver = ? and sender = ? )
"""
# ===================================CHAT=================================
CREATE_CHAT = """
INSERT INTO chats
VALUES (NULL , ? , ? , ?)
"""
GET_CHAT_ID ="""
SELECT id 
FROM chats
WHERE (user = ? AND user0 = ?) OR (user = ? AND user0 = ?)
"""
GET_USER_CHATS = """
SELECT c.id AS chat_id , u.id AS user_id , u.name , u.surname
FROM chats c
JOIN users u ON c.user = u.id OR c.user0 = u.id
WHERE (c.user = ? or c.user0 = ? ) AND u.id != ?
"""
GET_CHAT_MESSAGES = """
SELECT id , content , sender_id
FROM messages
WHERE chat_id = ? ORDER BY sent_at ASC
"""

UPDATE_CHAT_LAST_CONVERSATION = """
UPDATE chats SET last_txt = ?
WHERE id = ?
"""

GET_LAST_CHAT = """
SELECT c.id 
FROM messages m
JOIN chats c ON m.sender_id = c.user OR m.sender_id = c.user0
WHERE c.user = ? OR c.user0 = ?
ORDER BY m.sent_at
DESC LIMIT 1;
"""

GET_LAST_CHAT_INFO = """
SELECT  u.id AS user_id , u.name , u.surname
FROM chats c
JOIN users u ON c.user = u.id OR c.user0 = u.id
WHERE c.id = ? AND u.id != ?
"""

#==============================PERSONAL_INFO================================
INSERT_PERSONAL_INFO = """
INSERT INTO personal_info
VALUES (? , ?, ? , ? , ?, ?, ?, ?, ?, ? , ? , ? )
"""
UPDATE_PERSONAL_INFO = """
UPDATE personal_info 
SET ? = ? 
WHERE user_id = ?
"""
GET_PERSONAL_INFO = """
SELECT * 
FROM personal_info
WHERE user_id = ?
"""
CHECK_FOR_PERSONAL_INFO = """
SELECT * 
FROM personal_info
WHERE user_id = ?
"""
# ###################################CHANGE############################

GET_PASSWORD_QUERY = """SELECT password_hash FROM users 
WHERE id = ?"""

CHANGE_PASSWORD_QUERY = """UPDATE users 
SET password_hash = ? 
WHERE id = ?"""

FIND_EMAIL_QUERY = """ SELECT * 
FROM users 
WHERE email = ? """

CHANGE_EMAIL_QUERY = """UPDATE users 
SET email = ? 
WHERE id = ?
"""
USER_ALL_PICTURES = """SELECT pathTopic 
FROM user_picture
WHERE user_pic = ?
"""
GET_USER_ID_QUERY = """ SELECT id 
FROM users 
WHERE email = ?
"""