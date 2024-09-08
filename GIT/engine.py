from sqlmodel import SQLModel,create_engine,Session
from typing import Generator

sql_file_name="homework.db"
sql_url=f"sqlite:///{sql_file_name}"

engine=create_engine(sql_url,echo=True)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session()->Generator[Session,None,None]:
    with Session(engine) as session:
        yield session

create_db()