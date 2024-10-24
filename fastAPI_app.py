from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import unquote
import uuid  # 新增 uuid
import shutil  # 用於保存文件

# 初始化 FastAPI 應用
app = FastAPI()

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

# 創建文件存儲資料夾
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# PDF 上傳 API
@app.post("/upload_pdf")
async def upload_pdf(username: str = Form(...), file: UploadFile = File(...)):
    # 使用 UUID 生成唯一的文件名
    file_uuid = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]  # 取得文件的副檔名
    unique_file_name = f"{file_uuid}{file_extension}"  # 組合 UUID 與副檔名
    file_location = os.path.join(UPLOAD_FOLDER, unique_file_name)
    
    # 儲存文件到伺服器
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)  # 使用 shutil 儲存文件
    
    # 將文件資訊儲存到 SQLite
    db = SessionLocal()
    uploaded_file = UploadedFile(username=username, file_name=unique_file_name, file_path=file_location)
    db.add(uploaded_file)
    db.commit()
    db.close()
    
    return {"message": "File uploaded successfully", "file_name": unique_file_name}

# 列出使用者上傳的檔案 API
@app.get("/list_files")
def list_files(username: str):
    db = SessionLocal()
    files = db.query(UploadedFile).filter(UploadedFile.username == username).all()
    db.close()
    
    return [file.file_name for file in files]

# 提供 PDF 文件 API
@app.get("/get_pdf")
def get_pdf(file_name: str):
    db = SessionLocal()
    # decoded_file_name = unquote(file_name)  # URL 解碼
    file = db.query(UploadedFile).filter(UploadedFile.file_name == file_name).first()
    
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    # 提供 PDF 檔案給前端
    return FileResponse(path=file.file_path, media_type='application/pdf', filename=file.file_name)
