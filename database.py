from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///ngan_hang_cau_hoi.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CauHoi(Base):
    __tablename__ = "cau_hoi"

    id = Column(Integer, primary_key=True, index=True)
    mon_hoc = Column(String(50), nullable=False)       # Ví dụ: Tin học, Toán
    khoi_lop = Column(String(10), nullable=False)       # Ví dụ: 10, 11, 12
    dang_cau_hoi = Column(String(50), nullable=False)   # Dang_I, Dang_II, Dang_III, Tu_Luan
    muc_do = Column(String(20), nullable=False)         # Biet, Hieu, VanDung
    noi_dung = Column(Text, nullable=False)             # Nội dung câu hỏi
    
    # Đối với Dạng I (4 lựa chọn): A, B, C, D và DapAnDung ('A'/'B'/'C'/'D')
    # Đối với Dạng II (Đúng/Sai): 4 ý a, b, c, d
    dap_an_a = Column(Text, nullable=True)
    dap_an_b = Column(Text, nullable=True)
    dap_an_c = Column(Text, nullable=True)
    dap_an_d = Column(Text, nullable=True)
    dap_an_dung = Column(Text, nullable=True) 

Base.metadata.create_all(bind=engine)