from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine, select

class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    mood: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def add_message(session: Session, message: ChatMessage):
    session.add(message)
    session.commit()
    session.refresh(message)
    return message

def get_chat_history(session: Session, user_id: str, limit: int = 50):
    statement = select(ChatMessage).where(ChatMessage.user_id == user_id).order_by(ChatMessage.timestamp).limit(limit)
    return session.exec(statement).all()
