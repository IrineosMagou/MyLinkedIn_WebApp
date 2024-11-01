DROP TABLE personal_info;
DROP TABLE messages;
DROP TABLE chats;
DROP TABLE connections;
DROP TABLE users; 
DROP TABLE uploaded_articles;
DROP TABLE article_categories;
DROP TABLE interactions;
DROP TABLE uploaded_ads;
DROP TABLE article_interest;
DROP TABLE article_comments;
DROP TABLE user_picture;
DROP TABLE ad_interest;

CREATE TABLE users(
    id INTEGER PRIMARY KEY ,
    name TEXT ,
    surname TEXT ,
    password_hash TEXT ,
    email TEXT ,
    is_admin BOOLEAN DEFAULT 0 , 
    phone TEXT
);

CREATE TABLE personal_info(
    user_id INTEGER PRIMARY KEY ,
    age INTEGER ,
    profession TEXT ,
    experience TEXT ,
    education TEXT ,
    skills TEXT , 
    employment_agency TEXT ,
    is_age_p BOOLEAN DEFAULT 0 , 
    is_experience_p BOOLEAN DEFAULT 0 , 
    is_education_p BOOLEAN DEFAULT 0 , 
    is_skills_p BOOLEAN DEFAULT 0 , 
    is_employment_agency_p BOOLEAN DEFAULT 0 , 
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE user_picture(
    user_pic INTEGER PRIMARY KEY, 
    PathToPic TEXT , 
    FOREIGN KEY (user_pic) REFERENCES user (id)
);

CREATE TABLE connections (
    id INTEGER PRIMARY KEY,
    sender INTEGER,
    receiver INTEGER,
    state TEXT,
    created_at TEXT,
    accepted_at TEXT,
    rejected_at TEXT,
    FOREIGN KEY (sender) REFERENCES users(id),
    FOREIGN KEY (receiver) REFERENCES users(id)
);
CREATE INDEX idx_connections_state ON connections (state);

CREATE TABLE chats (
    id INTEGER PRIMARY KEY ,
    user INTEGER ,
    user0 INTEGER ,
    created_at TEXT 
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY ,
    chat_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    sent_at TEXT ,
    FOREIGN KEY (chat_id) REFERENCES chats (id),
    FOREIGN KEY (sender_id) REFERENCES users (id)
);

CREATE TABLE article_categories (
    id INTEGER PRIMARY KEY,
    category_name TEXT UNIQUE
);

INSERT INTO article_categories (category_name) VALUES
('Technology'),
('Sports'),
('Business'),
('Health'),
('Design'),
('Art'),
('Science');

CREATE TABLE uploaded_articles(
    id INTEGER PRIMARY KEY,
    uploader_id INTEGER ,
    title TEXT ,
    category_id INTEGER ,
    article TEXT ,
    path_to_media TEXT , 
    uploaded_at TEXT ,
    FOREIGN KEY (uploader_id) REFERENCES users(id)
    FOREIGN KEY (category_id) REFERENCES article_categories(id)
);

CREATE TABLE article_interest(
    id  INTEGER PRIMARY KEY ,
    article_id INT ,
    user_id INT ,
    interest_at TEXT ,
    FOREIGN KEY (article_id) REFERENCES uploaded_articles(id) ,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE article_comments(
    id INTEGER PRIMARY KEY ,
    user_id INT , 
    article_id INT , 
    comment TEXT ,
    comment_at TEXT ,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (article_id) REFERENCES uploaded_articles(id)
);

CREATE TABLE interactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    article_id INTEGER,
    interaction_value REAL,  -- Interaction strength (e.g., 1 for like, 0.5 for comment, etc.)
    interaction_type TEXT,  -- Type of interaction: view, like, comment, etc.
    interaction_at TEXT,    -- Timestamp of interaction
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (article_id) REFERENCES uploaded_articles(id)
);


CREATE TABLE uploaded_ads(
    id INTEGER PRIMARY KEY,
    uploader_id INTEGER ,
    title TEXT ,
    explanation TEXT ,
    uploaded_at TEXT ,
    FOREIGN KEY (uploader_id) REFERENCES users(id)
);
CREATE TABLE ad_interest(
    id  INTEGER PRIMARY KEY ,
    ad_id INT ,
    user_id INT ,
    interest_at TEXT ,
    FOREIGN KEY (ad_id) REFERENCES uploaded_ads(id) ,
    FOREIGN KEY (user_id) REFERENCES users(id)
);