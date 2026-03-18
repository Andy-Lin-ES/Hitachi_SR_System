from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_schema import Base, User, Fab, Tool, Subject

# 1. 連結我們剛剛建立的資料庫
engine = create_engine('sqlite:///hitachi_sr.db')
Session = sessionmaker(bind=engine)
session = Session()

def seed_basic_data():
    print("開始寫入基礎資料...")
    
    # 2. 準備要寫入的資料 (對應簡報中的真實案例)
    new_user = User(username="日立-黃其思", role="管理者") # [cite: 2, 28]
    new_fab = Fab(name="竹科-F12P7")                     # [cite: 45]
    new_tool = Tool(name="APCD21")                       # [cite: 66]
    new_subject = Subject(name="Modify")                 # [cite: 66]
    
    # 3. 將資料加入 Session 
    session.add_all([new_user, new_fab, new_tool, new_subject])
    
    # 4. 提交 (Commit) 到資料庫並儲存
    try:
        session.commit()
        print("✅ 基礎清單資料寫入成功！")
    except Exception as e:
        session.rollback() # 如果發生錯誤就退回，避免弄髒資料庫
        print(f"❌ 寫入失敗，可能是資料已存在。錯誤訊息：{e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_basic_data()