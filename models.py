from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 初始化資料庫
DATABASE_URL = "sqlite:///./pdf_files.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 資料庫模型
class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    file_name = Column(String, index=True)
    file_path = Column(String)

# 建立資料表
Base.metadata.create_all(bind=engine)

def save_uploaded_file(username, file_name, file_path):
    db = SessionLocal()
    uploaded_file = UploadedFile(username=username, file_name=file_name, file_path=file_path)
    db.add(uploaded_file)
    db.commit()
    db.close()

def list_files(username):
    db = SessionLocal()
    files = db.query(UploadedFile).filter(UploadedFile.username == username).all()
    db.close()
    return files
