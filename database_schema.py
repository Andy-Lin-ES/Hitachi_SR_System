from datetime import date, datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, DateTime
from sqlalchemy.orm import declarative_base

# 建立基礎類別
Base = declarative_base()

# ==========================================
# 1. 系統基礎設定與權限 [cite: 27]
# ==========================================
class User(Base):
    """【人員管理】[cite: 28]"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True) # 作業者姓名或帳號
    role = Column(String, nullable=False) # 權限設定：「管理者」、「一般使用者」 [cite: 28]

class Fab(Base):
    """【資料清單】- 廠區 [cite: 29]"""
    __tablename__ = 'fabs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True) # 例如：竹科-F12P7

class Tool(Base):
    """【資料清單】- 機台 [cite: 29]"""
    __tablename__ = 'tools'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True) # 例如：APCD21

class Subject(Base):
    """【資料清單】- 作業類型 [cite: 29]"""
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True) # 例如：Modify

class Holiday(Base):
    """【休祝日】[cite: 30]"""
    __tablename__ = 'holidays'
    id = Column(Integer, primary_key=True, autoincrement=True)
    holiday_date = Column(Date, nullable=False, unique=True) # 日期
    description = Column(String) # 例如：國慶日、颱風假、日立集團假日 [cite: 30]

# ==========================================
# 2. 業務紀錄與報表核心
# ==========================================
class FactoryAccessLog(Base):
    """【進出廠紀錄】[cite: 32, 44]"""
    __tablename__ = 'factory_access_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    worker_name = Column(String, nullable=False) # 作業者姓名 [cite: 43]
    fab_name = Column(String, nullable=False)    # 廠區(閘門) [cite: 43]
    entry_time = Column(DateTime, nullable=False)# 進廠時間 [cite: 43]
    exit_time = Column(DateTime, nullable=False) # 出廠時間 [cite: 43]

class ServiceRecord(Base):
    """【實際服務紀錄】[cite: 33, 76]"""
    __tablename__ = 'service_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)          # 作業日期 [cite: 76]
    worker_name = Column(String, nullable=False) # 作業者 [cite: 76]
    fab_name = Column(String, nullable=False)    # 廠區 [cite: 76]
    tool_id = Column(String, nullable=False)     # 機台 [cite: 76]
    subject = Column(String, nullable=False)     # 作業類型 [cite: 76]
    start_time = Column(DateTime, nullable=False)# 作業時間(開始) [cite: 76]
    end_time = Column(DateTime, nullable=False)  # 作業時間(結束) [cite: 76]
    
    # 時數計算結果 [cite: 123, 124, 125]
    weekday_hours = Column(Float, default=0.0)       # 平日(H)
    night_holiday_hours = Column(Float, default=0.0) # 夜間/假日(H)
    
    # 狀態標記 (防呆機制)
    is_sr_created = Column(Boolean, default=False)   # 是否已作成SR [cite: 191]

# ==========================================
# 3. 建立實體資料庫檔案
# ==========================================
if __name__ == "__main__":
    # 建立 SQLite 資料庫引擎 (echo=True 會在終端機印出底層的 SQL 語法，方便我們觀察)
    engine = create_engine('sqlite:///hitachi_sr.db', echo=True)
    
    # 根據上面的 Class 定義，正式在資料庫中建立所有的表
    print("正在建立資料庫表結構...")
    Base.metadata.create_all(engine)
    print("✅ 資料庫建置完成！")