from fastapi import  WebSocket
from typing import List , Dict
from threading import Lock
import asyncio
from queries.user_queries import CREATE_CHAT , GET_LAST_INSERT , GET_CHAT_ID , GET_USER_CHATS , GET_CHAT_MESSAGES , GET_LAST_CHAT , GET_LAST_CHAT_INFO
from datetime import datetime
import sqlite3
import json
# Manager to handle multiple WebSocket connections


class ChatManager:
    def __init__(self , db_conn):
        self.message_buffer: List[Dict] = []  # Buffer to store messages temporarily
        self.buffer_lock = Lock()  # Lock to prevent race conditions
        self.clients: Dict[str , WebSocket] = {}  # List of connected WebSocket clients
        self.db_conn = db_conn
        asyncio.create_task(self.flush_messages_periodically())

    async def connect(self, id:str, websocket: WebSocket):
        """Accepts a WebSocket connection and adds it to the list of clients."""
        await websocket.accept()
        self.clients[id] = websocket

    def disconnect(self, id: str ):
        del self.clients[id]

    async def broadcast(self, message: str):
        for client in self.clients:
            await client.send_text(message)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        message_json = json.dumps(message)  # Convert the message dictionary to a JSON string
        await websocket.send_text(message_json) 

    def add_message_to_buffer(self, chat_id: int, sender_id: int, content: str):
        with self.buffer_lock:
            self.message_buffer.append({"chat_id": chat_id, "sender_id": sender_id, "content": content})

    async def flush_messages_periodically(self):
        # print("FLUSH ΞΕΚΙΝΗΣΕ)
        while True:
            await asyncio.sleep(5)  # Flush every 5 seconds
            with self.buffer_lock:
                if self.message_buffer:
                    self.save_messages_to_db(self.message_buffer.copy())  # Copy buffer to avoid race conditions
                    self.message_buffer.clear()  # Clear buffer after saving

    def save_messages_to_db(self, messages: List[Dict]):
        """Saves messages from the buffer to the database in a single transaction."""
        # print("SAVE ΞΕΚΙΝΗΣΕ")
        with self.db_conn as conn:
            ts = datetime.utcnow() 
            cursor = conn.cursor()
            data_to_insert = [(msg["chat_id"], msg["sender_id"], msg["content"], ts) for msg in messages]
            cursor.executemany(
                "INSERT INTO messages (chat_id, sender_id, content, sent_at) VALUES (?, ?, ?, ?)",
                data_to_insert
            )
            conn.commit()
            
    def get_active_ws(self , id):
        return self.clients.get(id, None)

    def create_chat(
            self ,
            user : int ,
            user0: int ,
    ):
        ts = datetime.utcnow()
        with self.db_conn as conn:
            conn.execute(CREATE_CHAT ,(user , user0 , ts))
        chat_id = conn.execute(GET_LAST_INSERT).fetchone()

        return chat_id[0]

    def get_chat_id(
            self ,
            user : int ,
            user0 : int
    ):
        with self.db_conn as conn:
            chat = conn.execute(GET_CHAT_ID , (user , user0 , user0 , user)).fetchone()
            if not chat:
                new_chat = self.create_chat(user , user0)          
                return new_chat
        return chat[0]


    def get_chats(
            self ,
            id: int ,
    ):
        with self.db_conn as conn:
            conn.row_factory = sqlite3.Row
            chats = conn.execute(GET_USER_CHATS , (id ,id , id)).fetchall()
            if not chats :
                return None
        return [dict(row) for row in chats]


    def get_chat_messages(
            self ,
            room_id : int
    ):
        with self.db_conn as conn:
            messages = conn.execute(GET_CHAT_MESSAGES , (room_id ,)).fetchall()
            if not messages:
                return None
            
            formatted_messages = []
            for id , content, sender in messages:
                formatted_messages.append({
                    "id" : id ,
                    "content": content,
                    "sender": sender
                })

            return formatted_messages
        
    def get_last_chat(
            self ,
            user:int
    ):
        with self.db_conn as conn:
            last_chat = conn.execute(GET_LAST_CHAT,(user , user)).fetchone()
            if not last_chat:
                return None
            info = conn.execute(GET_LAST_CHAT_INFO , (last_chat[0] , user)).fetchone()
            chat_messages = self.get_chat_messages(last_chat[0])
            return {'messages': chat_messages , 'other_user' : info[0] , "last_chat" : last_chat[0]}
        
    def get_chat_info(
            self ,
            room_id : int ,
            user : int
    ):
        with self.db_conn as conn:
            info = conn.execute(GET_LAST_CHAT_INFO , (room_id, user)).fetchone()
            if info:
    # Create a dictionary with named keys
                info_dict = {
                    'id': info[0],
                    'name': info[1],
                    'surname': info[2]
                }
            else:
                info_dict = {}
            return info_dict

    