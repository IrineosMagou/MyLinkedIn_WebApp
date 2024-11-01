from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime , Float , func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker , declarative_base
from faker import Faker
from datetime import datetime
from passlib.context import CryptContext
import os
import random
import json
pwd_context = CryptContext(schemes=["bcrypt"] , deprecated = "auto")
def get_psswd_hash(psswd):
    return pwd_context.hash(psswd)

plain_password = 'passWord123'
DATABASE_URL = "sqlite:///../core.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Needed for SQLite

Base = declarative_base()

universities = [
    "Harvard University",
    "Stanford University",
    "Massachusetts Institute of Technology (MIT)",
    "University of Oxford",
    "University of Cambridge",
    "University of California, Berkeley",
    "ETH Zurich - Swiss Federal Institute of Technology",
    "University of Chicago",
    "Imperial College London",
    "University of Toronto",
    "National University of Singapore (NUS)",
    "Peking University",
    "Tsinghua University",
    "University of Melbourne",
    "University of Tokyo",
    "University of Edinburgh",
    "University of Amsterdam",
    "McGill University",
    "University of Sydney",
    "Seoul National University"
]
high_schools = [
    "Lincoln High School",
    "South High School",
    "Westwood High School",
    "Eastview High School",
    "Central High School",
    "Riverside High School",
    "Green Valley High School",
    "Maple Leaf High School",
    "Sunnydale High School",
    "Oakwood High School",
    "Crestwood High School",
    "Hilltop High School",
    "Springfield High School",
    "Pinecrest High School",
    "Northview High School",
    "Silver Creek High School",
    "Mountain Ridge High School",
    "Lakeside High School",
    "Forest Hill High School",
    "Willow Creek High School"
]
job_skills = [
    "Communication",
    "Teamwork",
    "Problem Solving",
    "Critical Thinking",
    "Project Management",
    "Time Management",
    "Adaptability",
    "Technical Proficiency",
    "Data Analysis",
    "Customer Service",
    "Leadership",
    "Negotiation",
    "Creativity",
    "Programming",
    "Attention to Detail",
    "Sales",
    "Marketing",
    "Financial Analysis",
    "Research",
    "Social Media Management"
]
job_experiences = [
    "Software Developer at XYZ Corp (2020 - Present)",
    "Data Analyst at ABC Inc. (2018 - 2020)",
    "Project Manager at Tech Solutions (2016 - 2018)",
    "Marketing Coordinator at Creative Agency (2015 - 2016)",
    "Customer Service Representative at Retail Co. (2014 - 2015)",
    "Sales Associate at Local Store (2013 - 2014)",
    "Intern at Non-Profit Organization (Summer 2012)",
    "Research Assistant at University (2011 - 2012)",
    "Graphic Designer at Design Studio (2010 - 2011)",
    "Web Developer at Startup (2009 - 2010)",
    "Content Writer at Online Magazine (2008 - 2009)",
    "Human Resources Intern at Corporation (Summer 2007)",
    "Financial Analyst at Investment Firm (2006 - 2008)",
    "Technical Support Specialist at IT Services (2005 - 2006)",
    "Operations Manager at Logistics Company (2004 - 2005)",
    "Quality Assurance Tester at Software Firm (2003 - 2004)",
    "Database Administrator at Data Solutions (2002 - 2003)",
    "SEO Specialist at Marketing Agency (2001 - 2002)",
    "Network Engineer at Telecom Company (2000 - 2001)",
    "Teacher at Local High School (1999 - 2000)"
]
job_titles = [
    "Software Developer",
    "Data Scientist",
    "Marketing Manager",
    "Sales Representative",
    "Project Manager",
    "Graphic Designer",
    "Financial Analyst",
    "Customer Support Specialist",
    "Human Resources Manager",
    "Network Administrator",
    "Web Developer",
    "Content Writer",
    "Research Scientist",
    "Product Manager",
    "UX/UI Designer",
    "Operations Manager",
    "Social Media Specialist",
    "Database Administrator",
    "Business Analyst",
    "Compliance Officer",
    "Systems Analyst",
    "Quality Assurance Tester",
    "IT Support Technician",
    "Public Relations Specialist",
    "Brand Strategist",
    "Event Coordinator",
    "SEO Specialist",
    "Copywriter",
    "Executive Assistant",
    "Legal Assistant"
]
art_cat =[
    "Technology",
    "Sports",
    "Business",
    "Health",
    "Design",
    "Science"
]
def generate_random_job_title():
    return random.choice(job_titles)

def generate_random_categories():
    return random.choice(art_cat)

def generate_education():
    education_level = random.choice(["High School", "Bachelor's Degree", "Master's Degree", "PhD"])
    
    if education_level == "High School":
        institution = random.choice(high_schools)
    else :
        institution = random.choice(universities)
    
    return institution


def generate_job_skills(num_skills=5):
    return random.sample(job_skills, min(num_skills, len(job_skills)))

def generate_random_experience():
    years = random.randint(0, 10)
    has_half_year = random.choice([True, False])
    if has_half_year:
        experience = f"{years} years, 6 months"
    else:
        experience = f"{years} years"

    return experience

# Define your models
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    password_hash = Column(String)
    email = Column(String, unique=True)
    is_admin = Column(Boolean, default=False)
    phone = Column(String)

class PersonalInfo(Base):
    __tablename__ = 'personal_info'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    age = Column(Integer)
    profession = Column(String)
    experience = Column(String)
    education = Column(String)
    skills = Column(String)  # Consider using a different model for complex data types
    employment_agency = Column(String)
    is_age_p = Column(Boolean, default=False)
    is_experience_p = Column(Boolean, default=False)
    is_education_p = Column(Boolean, default=False)
    is_skills_p = Column(Boolean, default=False)
    is_employment_agency_p = Column(Boolean, default=False)

class UserPicture(Base):
    __tablename__ = 'user_picture'

    user_pic = Column(Integer, ForeignKey('users.id'), primary_key=True)
    PathToPic = Column(String)

class Connection(Base):
    __tablename__ = 'connections'

    id = Column(Integer, primary_key=True)
    sender = Column(Integer, ForeignKey('users.id'))
    receiver = Column(Integer, ForeignKey('users.id'))
    state = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    accepted_at = Column(DateTime, nullable=True)
    rejected_at = Column(DateTime, nullable=True)

class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    user = Column(Integer)  # Consider changing to ForeignKey if needed
    user0 = Column(Integer)  # Consider changing to ForeignKey if needed
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    sender_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    sent_at = Column(DateTime, default=datetime.utcnow)

class ArticleCategories(Base):
    __tablename__ = 'article_categories'

    id = Column(Integer, primary_key=True)
    category_name = Column(String)

class UploadedArticle(Base):
    __tablename__ = 'uploaded_articles'

    id = Column(Integer, primary_key=True)
    uploader_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    category_id = Column(Integer , ForeignKey('article_categories.id'))
    article = Column(String)
    path_to_media = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class ArticleInterest(Base):
    __tablename__ = 'article_interest'

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('uploaded_articles.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    interest_at = Column(DateTime, default=datetime.utcnow)

class ArticleComment(Base):
    __tablename__ = 'article_comments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    article_id = Column(Integer, ForeignKey('uploaded_articles.id'))
    comment = Column(String)
    comment_at = Column(DateTime, default=datetime.utcnow)

class Interactions(Base):
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    article_id = Column(Integer, ForeignKey('uploaded_articles.id'))
    interaction_value = Column(Float)
    interaction_type = Column(String)
    interaction_at = Column(DateTime, default=datetime.utcnow)



class UploadedAd(Base):
    __tablename__ = 'uploaded_ads'

    id = Column(Integer, primary_key=True)
    uploader_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    explanation = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class AdInterest(Base):
    __tablename__ = 'ad_interest'

    id = Column(Integer, primary_key=True)
    ad_id = Column(Integer, ForeignKey('uploaded_ads.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    interest_at = Column(DateTime, default=datetime.utcnow)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Create a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
fake = Faker()


num_users = 500
num_categories = 7

# Initialize lists for each category
category_lists = {i: [] for i in range(1, num_categories + 1)}

# Generate a random number of categories for each user and assign the user to those categories
for user_id in range(1, num_users + 1):
    num_categories_for_user = random.randint(1, 5)  # Randomly pick how many categories to assign
    categories_for_user = random.sample(range(1, 8), num_categories_for_user)  # Pick random categories
    
    # Add the user to the corresponding category lists
    for category in categories_for_user:
        category_lists[category].append(user_id)


def populate_db():
    db = SessionLocal()
    
# Populate users
    users = []
    for _ in range(num_users):  # Adjust the number of users to create
        hashed_password = get_psswd_hash(plain_password)
        user = User(
            name=fake.first_name(),
            surname=fake.last_name(),
            password_hash=hashed_password,
            email=fake.unique.email(),
            is_admin=False,
            phone=fake.phone_number(),
        )
        users.append(user)
    db.add_all(users)
    db.commit()

# Populate personal_info
    for user in users:
        personal_info = PersonalInfo(
            user_id=user.id,
            age=fake.random_int(min=18, max=65),
            profession=generate_random_job_title(),
            experience=generate_random_experience(),
            education=generate_education(),  # Convert dict to JSON string
            skills=', '.join(generate_job_skills()),  # Convert list to string
            employment_agency=fake.company(),
            is_age_p=fake.boolean(),
            is_experience_p=fake.boolean(),
            is_education_p=fake.boolean(),
            is_skills_p=fake.boolean(),
            is_employment_agency_p=fake.boolean(),
        )
        db.add(personal_info)
    db.commit()

# Populate user pictures
    for user in users:
        path_to_pic = f"/pictures/{user.id}.jpg" 
        user_picture = UserPicture(
            user_pic=user.id,
            PathToPic=path_to_pic,
        )
        db.add(user_picture)
    db.commit()

# Populate connections
    connections = []
    for _ in range(len(users) * 2):  # Create some random connections
        sender = fake.random_element(users).id
        receiver = fake.random_element(users).id
        while sender == receiver:  # Ensure different sender and receiver
            receiver = fake.random_element(users).id
            
        connection = Connection(
            sender=sender,
            receiver=receiver,
            state=fake.random_choices(elements=["Pending", "Accepted", "Rejected"], length=1)[0],
        )
        connections.append(connection)

    db.add_all(connections)
    db.commit()

    # BASE_MEDIA_DIR = "../media/"

    # def create_article_media_directory(article_id):
    #     article_dir = os.path.join(BASE_MEDIA_DIR, f"article{article_id}")
    #     if not os.path.exists(article_dir):
    #         os.makedirs(article_dir)
    #     return article_dir
    
# Populate Article
    articles =[]
    for _ in range(300):
            category_id = random.choice(list(category_lists.keys()))
            uploader_id = random.choice(category_lists[category_id])
        # Assume `user.categories` holds a list of categories the user is part o
            article = UploadedArticle(
                uploader_id=uploader_id,
                title=fake.sentence(),
                category_id=random.randint(1, 7),  # Choose a category from the user's preferences
                article=fake.text(max_nb_chars=500),
                path_to_media='',
                uploaded_at=fake.date_time_this_year(),
            )
            db.add(article)
            db.commit()
            # Create a media directory for the article after committing to get its ID
            # article_media_dir = create_article_media_directory(article.id)
            # article.path_to_media = article_media_dir
            articles.append(article)
    db.commit()

# Function to get the category_id based on article_id
    def get_category_id(article_id):
        article = db.query(UploadedArticle).filter(UploadedArticle.id == article_id).first()
        return article.category_id if article else None

# Populate article interests
    for _ in range(2250):  # Adjust the number of interests to create
        art_id = fake.random_int(min=1, max=len(articles))
        category = get_category_id(art_id)
        interest = ArticleInterest(
            article_id=art_id,
            user_id=random.choice(category_lists[category]),
            interest_at=fake.date_time_this_year(),
        )
        db.add(interest)

    db.commit()

    # Populate article comments
    for _ in range(2450):  # Adjust the number of comments to create
        art_id = fake.random_int(min=1, max=len(articles))
        category = get_category_id(art_id)
        comment = ArticleComment(
            user_id=random.choice(category_lists[category]),
            article_id=art_id,
            comment=fake.sentence(),
            comment_at=fake.date_time_this_year(),
        )
        db.add(comment)

# =============Fill the interactions table==================
    Session = sessionmaker(bind=engine)
    session = Session()
    def populate_interactions():

        interests = session.query(ArticleInterest).all()
        comments = session.query(ArticleComment).all()

        for interest in interests:
            interaction = Interactions(
                user_id=interest.user_id,
                article_id=interest.article_id,
                interaction_value=1.0,  # Assume a like for interests
                interaction_type='like',  # Set the type as 'like'
            )
            session.add(interaction)

 

        for comment in comments:
            interaction = Interactions(
                user_id=comment.user_id,
                article_id=comment.article_id,
                interaction_value=0.8,  # Assign a interaction_value for comments
                interaction_type='comment',  # Set the type as 'comment'
            )
            session.add(interaction)

        # Optionally, add views for all interests and comments
        for interest in interests:
            interaction = Interactions(
                user_id=interest.user_id,
                article_id=interest.article_id,
                interaction_value=0.2,  # interaction_Value for view
                interaction_type='view',  # Set the type as 'view'
            )
            session.add(interaction)

        for comment in comments:
            interaction = Interactions(
                user_id=comment.user_id,
                article_id=comment.article_id,
                interaction_value=0.2,  # interaction_Value for view
                interaction_type='view',  # Set the type as 'view'
            )
            session.add(interaction)

        # Commit the changes to the database
        session.commit()
        print("Interactions populated successfully!")

    populate_interactions()

    # Populate uploaded ads
    for user in users:
        ad = UploadedAd(
            uploader_id=user.id,
            title=fake.sentence(),
            explanation=fake.text(max_nb_chars=200),
            uploaded_at=fake.date_time_this_year(),
        )
        db.add(ad)

    db.commit()

    # Populate ad interests
    for _ in range(15):  # Adjust the number of interests to create
        interest = AdInterest(
            ad_id=fake.random_int(min=1, max=len(users)),
            user_id=fake.random_element(users).id,
            interest_at=fake.date_time_this_year(),
        )
        db.add(interest)

    db.commit()

    print("Database populated successfully!")

if __name__ == "__main__":
    populate_db()
    

    # # Populate chats and messages
    # for _ in range(5):  # Adjust the number of chats to create
    #     chat = Chat(user=fake.random_element(users).id, user0=fake.random_element(users).id)
    #     db.add(chat)
    #     db.commit()  # Commit the chat first to get its ID
        
    #     for _ in range(3):  # Each chat will have some messages
    #         message = Message(
    #             chat_id=chat.id,
    #             sender_id=fake.random_element(users).id,
    #             content=fake.text(max_nb_chars=200),
    #             sent_at=fake.date_time_this_year(),
    #         )
    #         db.add(message)

    # db.commit()