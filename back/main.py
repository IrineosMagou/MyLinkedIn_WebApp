import json
import asyncio
from fastapi.security import OAuth2PasswordRequestForm
import sqlite3 
from fastapi import FastAPI , Depends , HTTPException ,  UploadFile, Response , WebSocket  , File , Form ,Security 
from fastapi.middleware.cors import CORSMiddleware
from queries.user_queries import *
from dependencies import establish_conn
from validation.passwd_hash import *
from validation.token_val import *
from fastapi.staticfiles import StaticFiles
from classes.utils import *
from models.AdsModels import *
from models.ArticleModels import *
from models.models_user import *
app = FastAPI()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pictures_dir = "/mnt/c/Users/User/Desktop/201700208_ΤΕΔ24/back/pictures"
media_dir = "/mnt/c/Users/User/Desktop/TED24/201700208_ΤΕΔ24/media"
app.mount("/pictures", StaticFiles(directory="pictures"), name="pictures")
app.mount("/media", StaticFiles(directory="media"), name="media")
comm = None
# ====================================================================================STARTUP====DB_CONNECTION
# ============================================================================================================
@app.on_event("startup")
async def startup_event():
    try:
        # Attempt to establish a database connection
        with sqlite3.connect("core.db") as conn:
            conn.execute("SELECT 1")  # Perform a simple query
            print("Database connection successful")
        global comm
        comm = ChatManager(conn)
        asyncio.create_task(comm.flush_messages_periodically())
        
    except sqlite3.Error as e:
        print("Failed to connect to the database:", str(e))
        raise

@app.on_event("shutdown")
async def shutdown_event():
    print("Application shutting down")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

currentUser = Annotated[str , Depends(get_current_user)]

#CREATE_USER
@app.post("/create_user/", status_code=201)
async def create_user(name: Annotated[str , Form()] , 
                      surname: Annotated[str , Form()],
                      password: Annotated[str , Form()],
                      email: Annotated[str , Form()],
                      phone: Annotated[str , Form()],
                      response: Response ,picture :Optional[UploadFile] = File(None), conn = Depends(establish_conn)):
        new_user = New_User(
            name = name ,
            surname = surname ,
            password=password ,
            email=email,
            phone=phone,
        )
        create_new_user = NewUser(conn)
        access_token = create_new_user.create_user(new_user)
        if access_token:
            create_new_user.profile_picture(picture)
            return {"message": "User created successfully","access_token": access_token, "token_type": "bearer"}
        else:
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
            return {"email exists" : True}
    
#PROFILE-PICTURE
@app.post("/user_profile/picture" , status_code=201)
async def picture_insert( current_user: currentUser , picture: UploadFile , conn = Depends(establish_conn)):#current user has the id that "get_current_users" return
        new_user = NewUser(conn)
        new_user.profile_picture(picture , current_user['user'])

#SIGN_IN
@app.post("/token" , response_model=Token)
async def signIn(form_data: Annotated[OAuth2PasswordRequestForm , Depends()], conn = Depends(establish_conn)):
    user = SignIn(conn)
    access_token = user.check_credentials(form_data)
    return {"access_token": access_token, "token_type": "bearer"}

#CONNECTIONS_OF_THE_USER
@app.get("/user_conn" , status_code=200)
async def user_conn( current_user: currentUser  ,  conn = Depends(establish_conn)):
    user = UserSearch(conn)
    results = user.connections_of_user(current_user['user'])
    return {"data": results}

#SEARCH_FOR_USERS
@app.post("/user_search" , status_code=200)
async def user_search( current_user : currentUser , profess : UserSearchModel , response :Response, conn = Depends(establish_conn)):
    search = UserSearch(conn)
    res = search.search_user(profess , current_user['user'])
    if not res:
        response.status_code = status.HTTP_404_NOT_FOUND
    return {"data" : res }
            
# USER_VIEW
@app.get("/user_view/{user_id}" , status_code = 200)
async def user_view(current_user: currentUser  ,user_id: int ,  response :Response,  conn = Depends(establish_conn)):
    if current_user['is_admin']:
        adm = Admin(conn)
        res = adm.user_view(user_id)
    else:
        view = UserSearch(conn)
        res = view.user_view(current_user['user'] , user_id)
        if not res:
            response.status_code = status.HTTP_404_NOT_FOUND
    return {'data' : res}
    
#CONNECTION_REQUEST 
@app.post("/connection_request" , status_code=201 )
async def connection_req(handle : TokenData , current_user: currentUser , conn = Depends(establish_conn)):  #TokenData just cause of teh type int
    con = Connections(conn)
    message = con.connection_request(current_user['user'] , handle.id)
    return message        

# HANDLE_CONNECTION_REQUEST  
@app.post("/handle_request" , status_code=200 )
async def handle_request( handle : ConnectionHandle , current_user: currentUser , conn = Depends(establish_conn)):
        con = Connections(conn)
        handle_req = con.handle_request(current_user['user'], handle.id , handle.handle)
        return handle_req

# USER_NOTIFICATIONS 
@app.get("/user_notifications" , status_code=200 )
async def connection_req(current_user: currentUser , response :Response, conn = Depends(establish_conn)):  
    acc = UserAccount(conn)
    notification = acc.notifications(current_user['user'])
    if not notification:
        response.status_code = status.HTTP_404_NOT_FOUND
    return notification

# ===============================================
#ARTICLES
# ===============================================
# USER_ARTICLES_VIEW
@app.get("/view_articles" , status_code = 200)
async def view_articles(current_user : currentUser , response :Response , conn = Depends(establish_conn)):
    art = Articles(conn)
    articles = art.user_articles(current_user['user'])
    if not articles:
        response.status_code = status.HTTP_404_NOT_FOUND
    return {"data" : articles }

# USER_ARTICLES_UPLOAD    
@app.post("/upload_article" , status_code = 201)
async def upload_article(current_user : currentUser , title : Annotated[str , Form()]  , category : Annotated[str , Form()], 
                         article : Annotated[str , Form()] , id : Optional[Annotated[int , Form()]] = Form(None) , media :list[UploadFile] = File(None),conn = Depends(establish_conn)):
    up = Articles(conn)
    if id :
        upload = up.upload_articles( current_user['user'] , title ,  article , category , art_id=id , media=media)
    else:
        upload = up.upload_articles(current_user['user'] , title ,  article ,category, media=media)
    return upload

# ARTICLE_FULL_VIEW   
@app.get("/full_article/{article_id}" , status_code = 200)
async def full_article(_:  currentUser , article_id : int , conn = Depends(establish_conn)):
    full = Articles(conn)
    article = full.full_article(article_id)
    return {"data" : article}

#ARTICLE_INTEREST  

@app.post("/article_interest" , status_code = 201)
async def article_interest(current_user : currentUser , article : InterestArticle , conn = Depends(establish_conn)):
    interest = Articles(conn)
    int = interest.article_interest(current_user['user'] , article.id , article.interest)
    return {"data" : int}
#ARTICLE_COMMENT  
@app.post("/comment_article" , status_code = 201)
async def article_com(current_user: currentUser , comment : CommentArticle , conn = Depends(establish_conn)):
    com = Articles(conn)
    msg = com.article_comment(current_user['user'] , comment.article_id , comment.comment)
    return{"Message": msg}

@app.get("/get_my_articles")
async def my_article(current_user : currentUser , conn = Depends(establish_conn)):
    art = Articles(conn)
    titles = art.my_articles(current_user['user'])
    if not titles:
        return {"Message" : " No uploaded articles to show"}
    return {"data" : titles}


# ================================================================
# CHAT
# WEB_SOCKET  
# ================================================================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket , conn = Depends(establish_conn)):
    token = websocket.query_params.get("token") 
    user = await get_current_user_ws(token , conn)
    await comm.connect(str(user) , websocket)
    while True:
        raw_data = await websocket.receive_text()
        parsed_data = json.loads(raw_data)
        chat_id = parsed_data["data"].get("chat_id")
        receiver_id = parsed_data["data"].get("receiver_id")
        message_text = parsed_data["data"].get("text")
        print(f'This the evverything from the receive message : chat{chat_id} , receiver {receiver_id} , message : {message_text}' )
        active = comm.get_active_ws(str(receiver_id))
        if active:
            await comm.send_personal_message(message_text , active)  
        comm.add_message_to_buffer(chat_id , user , message_text)
        # await websocket.send_text(f"Message text was: {message_text}")


@app.get("/chatroom/{user_id}" , status_code = 200)
async def chatroom(current_user : currentUser , user_id : int , conn = Depends(establish_conn)):
    chat = ChatManager(conn)
    chat_id = chat.get_chat_id(current_user['user'] , user_id )
    return {"chat_id" : chat_id}

@app.get("/get_user_chats" , status_code = 200)
async def get_user_chats(current_user : currentUser , conn = Depends(establish_conn)):
    chat = ChatManager(conn)
    chats = chat.get_chats(current_user['user'])
    return {"data" : chats}

@app.get("/get_chat_messages/{room_id}" , status_code = 200)
async def chat_messages(current_user: currentUser , room_id : int , conn = Depends(establish_conn)):
    chat = ChatManager(conn)
    messages = chat.get_chat_messages(room_id)
    if messages is None:
        return {"messages": [] , "id" : current_user['user']} 
    return {"messages" : messages , "id" : current_user['user'] }

@app.get("/get_last_chat" , status_code = 200)
async def get_last(current_user : currentUser ,conn = Depends(establish_conn)):
    chat = ChatManager(conn)
    messages = chat.get_last_chat(current_user['user'])
    if messages is None:
        return {"messages": []} 
    return {"info" : messages }

@app.get("/get_chat_info/{room_id}" , status_code = 200)
async def get_last(current_user : currentUser , room_id : int ,conn = Depends(establish_conn)):
    chat = ChatManager(conn)
    info = chat.get_chat_info(room_id , current_user['user'] )
    return{'info' : info}


# ====================================================================================
#ADS
# =====================================================================================
# UPLOAD_AD
@app.post("/upload_ad" , status_code = 201)
async def upload_ad(current_user :currentUser , ad : UploadAd ,  conn=Depends(establish_conn)):
    ads = Ads(conn)
    upload = ads.upload_ads(current_user['user'] , ad)
    return {'Message' : upload}

@app.get("/view_ads" , status_code = 200)
async def view_ads(current_user : currentUser , response :Response , conn = Depends(establish_conn)):
    art = Ads(conn)
    ads = art.user_ads(current_user['user'])
    if not ads:
        response.status_code = status.HTTP_404_NOT_FOUND
    return {"data" : ads }

@app.get("/full_ad/{ad_id}" , status_code = 200)
async def full_ad(_:  currentUser , ad_id : int , conn = Depends(establish_conn)):
    full = Ads(conn)
    ad = full.full_ad(ad_id)
    return {"data" : ad }


@app.get("/get_my_ads")
async def my_ads(current_user : currentUser , conn = Depends(establish_conn)):
    ad = Ads(conn)
    titles = ad.my_ads(current_user['user'])
    if not titles:
        return {"Message" : " No uploaded articles to show"}
    return {"data" : titles}

# AD_INTEREST  
@app.post("/ad_interest" , status_code = 201)
async def ad_interest(current_user : currentUser , ad : InterestAd , conn = Depends(establish_conn)):
    interest = Ads(conn)
    int = interest.ad_interest(current_user['user'] , ad.id , ad.interest)
    return {"data" : int}

# AD_COMMENT  
@app.post("/comment_ad" , status_code = 201)
async def ad_com(current_user: currentUser , comment : CommentAd , conn = Depends(establish_conn)):
    com = Ads(conn)
    msg = com.ad_comment(current_user['user'] , comment.ad_id , comment.comment)
    return{"Message": msg}






# =========================================================================
#ACCOUNT INFO
# ==========================================================================
@app.post("/personal-info/" )
async def save_personal_info(current_user  : currentUser , info: Personal_Info , conn = Depends(establish_conn)):
    set_information = PersonalInfo(conn)
    success = set_information.info_management(current_user['user'] , info)
    if success:
        return {"message": "Personal info saved"}
    return{"message" : "ggg"}

@app.get("/get_personal_info")
async def get_personal_info(current_user  : currentUser , conn = Depends(establish_conn)):
    get_info = PersonalInfo(conn)
    user_info = get_info.personal_info_view(current_user['user'])
    return {"info" : user_info}

# CHANGE_PΑSSWD 
@app.post("/change_password" , status_code=200 )
async def change_password(current_user: currentUser ,password: ChangePasswd, conn = Depends(establish_conn)):
    new_pass = Changes(conn)
    print(f' This is the type of user {type(current_user)}')
    message = new_pass.change_password(current_user['user'] , password)
    if not message :
        raise HTTPException(status_code=400, detail="The current code you provided is wrong")
    return message

# CHANGE_USΕRNΑME
@app.post("/change_email" , status_code=200 )
async def change_mail(current_user: currentUser , mail : ChangeMail, conn = Depends(establish_conn)):
    email = Changes(conn)
    message = email.change_email(current_user['user'] , mail.new_mail)
    if not message :
        raise HTTPException(status_code=400, detail="There is account with this email")
    return message
 


#===========================================================
#ADMIN
#===========================================================
@app.get("/users_list" , dependencies=[Security(get_current_user, scopes=["admin"])], status_code = 200)
async def user_list(_ : currentUser , conn = Depends(establish_conn)):
    adm = Admin(conn)
    users = adm.get_user_list()
    return {'users' : users}

@app.get("/user_data/{user_id}" , dependencies=[Security(get_current_user, scopes=["admin"])], status_code = 200)
async def user_list(_ : currentUser , user_id : int, conn = Depends(establish_conn)):
    adm = Admin(conn)
    user_data = adm.user_data(user_id)
    
    return {'user' : user_data}

@app.get("/user_data/xml/{user_id}", dependencies=[Security(get_current_user, scopes=["admin"])], status_code=200)
async def user_list_xml(
    _: currentUser,
    user_id: int,
    conn=Depends(establish_conn)
):
    adm = Admin(conn)
    user_data = adm.user_data(user_id)
    xml_content = adm.user_data_to_xml(user_data)
    return Response(content=xml_content, media_type="application/xml")