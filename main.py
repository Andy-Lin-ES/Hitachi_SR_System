from fastapi import FastAPI, Depends
from pydantic import BaseModel
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database_schema import Fab, Tool, Subject, User, ServiceRecord

# ==========================================
# 1. API 網頁介面美化與繁體中文化設定
# ==========================================
app = FastAPI(
    title="日立維修服務報告書系統 API",
    description="""
    這是一個專為 Hitachi SR 系統打造的後端 API 測試與開發文件介面。
    您可以在此查看所有功能說明，並直接發送測試資料寫入 SQLite 資料庫。

    ### 核心功能模組：
    * **系統狀態**：確認伺服器連線狀況。
    * **基礎設定**：提供前端表單所需的下拉選單資料（廠區、機台等）。
    * **維修紀錄**：提交服務報告，並內建自動計算「平日」與「夜間/假日」時數的商業邏輯。
    """,
    version="1.0.0",
    # 隱藏下方用不到的 Data Models 區塊，保持畫面清爽
    swagger_ui_parameters={"defaultModelsExpandDepth": -1} 
)

engine = create_engine('sqlite:///hitachi_sr.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 資料接收格式定義 (Pydantic Model)
# ==========================================
class RecordSubmit(BaseModel):
    date: date
    worker_name: str
    fab_name: str
    tool_id: str
    subject: str
    start_time: datetime
    end_time: datetime
    is_workday: bool = True  # 預設為工作日

# ==========================================
# 核心邏輯：特殊工時計算 (維持原樣，不更動)
# ==========================================
def custom_round_hours(td: timedelta) -> float:
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    if 0 <= minutes <= 14:
        added_minutes = 0
    elif 15 <= minutes <= 29:
        added_minutes = 30
    elif 30 <= minutes <= 44:
        added_minutes = 30
    elif 45 <= minutes <= 59:
        added_minutes = 60
    else:
        added_minutes = 0
    return hours + (added_minutes / 60.0)

def calculate_service_hours(start_time: datetime, end_time: datetime, is_workday: bool):
    total_td = end_time - start_time
    total_hours = custom_round_hours(total_td)
    weekday_hours = 0.0
    night_holiday_hours = 0.0
    
    if is_workday:
        standard_start = start_time.replace(hour=9, minute=0, second=0, microsecond=0)
        standard_end = start_time.replace(hour=17, minute=30, second=0, microsecond=0)
        actual_weekday_start = max(start_time, standard_start)
        actual_weekday_end = min(end_time, standard_end)
        
        if actual_weekday_start < actual_weekday_end:
            weekday_td = actual_weekday_end - actual_weekday_start
            weekday_hours = custom_round_hours(weekday_td)
            night_td = total_td - weekday_td
            night_holiday_hours = custom_round_hours(night_td)
        else:
            night_holiday_hours = custom_round_hours(total_td)
            
        if (weekday_hours + night_holiday_hours) > total_hours:
            weekday_hours -= 0.5
    else:
        night_holiday_hours = custom_round_hours(total_td)
        
    return weekday_hours, night_holiday_hours

# ==========================================
# API 端點 (加上了 Tags, Summary 與 Description)
# ==========================================
@app.get(
    "/", 
    tags=["系統狀態"], 
    summary="檢查伺服器狀態",
    description="用來確認後端 Uvicorn 伺服器是否正常運作中。"
)
def read_root():
    return {"message": "✅ 日立維修服務報告書系統 API 已經成功啟動！"}

@app.get(
    "/api/options", 
    tags=["基礎設定"], 
    summary="取得表單下拉選單資料",
    description="從資料庫查詢所有的廠區 (Fab)、機台 (Tool)、服務項目 (Subject) 與工程師 (User) 列表，回傳給前端渲染表單使用。"
)
def get_form_options(db: Session = Depends(get_db)):
    fabs = [fab.name for fab in db.query(Fab).all()]
    tools = [tool.name for tool in db.query(Tool).all()]
    subjects = [subject.name for subject in db.query(Subject).all()]
    users = [user.username for user in db.query(User).all()]
    return {"fabs": fabs, "tools": tools, "subjects": subjects, "users": users}

@app.post(
    "/api/records", 
    tags=["維修紀錄"], 
    summary="提交維修服務報告",
    description="接收前端傳來的維修表單資料。系統會自動根據 `start_time` 與 `end_time` 計算出『平日時數』與『夜間/假日時數』，最後將完整紀錄寫入 SQLite 資料庫。"
)
def submit_service_record(record: RecordSubmit, db: Session = Depends(get_db)):
    """接收前端傳來的表單，計算時數後存入資料庫"""
    # 1. 執行時數計算
    weekday_h, night_holiday_h = calculate_service_hours(record.start_time, record.end_time, record.is_workday)
    
    # 2. 建立資料庫物件
    db_record = ServiceRecord(
        date=record.date,
        worker_name=record.worker_name,
        fab_name=record.fab_name,
        tool_id=record.tool_id,
        subject=record.subject,
        start_time=record.start_time,
        end_time=record.end_time,
        weekday_hours=weekday_h,
        night_holiday_hours=night_holiday_h
    )
    
    # 3. 寫入資料庫
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return {
        "message": "✅ 紀錄新增成功！",
        "計算結果": {
            "平日時數": weekday_h,
            "夜間/假日時數": night_holiday_h
        }
    }