from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from export_word import tao_file_word_de_thi
import os

app = FastAPI()

@app.post("/api/tao-ma-tran")
async def tao_ma_tran_de_thi(
    mon_hoc: str = Form(...),
    khoi_lop: str = Form(...),
    loai_kiem_tra: str = Form(...),
    thoi_gian: int = Form(...),
    dang1_biet: int = Form(0),
    dang1_hieu: int = Form(0),
    dang1_vandung: int = Form(0),
    dang2_biet: int = Form(0),
    dang2_hieu: int = Form(0),
    dang2_vandung: int = Form(0),
    file_ppct: UploadFile = File(None)
):
    # Cấu hình ma trận lấy từ form
    ma_tran_config = {
        "mon_hoc": mon_hoc,
        "khoi_lop": khoi_lop,
        "loai_kiem_tra": loai_kiem_tra,
        "thoi_gian": thoi_gian,
        "ma_tran": {
            "dang_1_nhieu_lua_chon": {"biet": dang1_biet, "hieu": dang1_hieu, "vandung": dang1_vandung},
            "dang_2_dung_sai": {"biet": dang2_biet, "hieu": dang2_hieu, "vandung": dang2_vandung}
        }
    }

    # Tiến hành sinh file Word dựa trên dữ liệu ma trận
    file_word_path = tao_file_word_de_thi(ma_tran_config, "De_Thi_Sinh_Tu_Dong.docx")

    # Trả trực tiếp file Word (.docx) về cho trình duyệt để người dùng tải xuống
    return FileResponse(
        path=file_word_path, 
        filename="De_Thi_CV7991.docx", 
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    from fastapi.responses import HTMLResponse

# Thêm route cho trang chủ
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head><title>Nga Tạo Đề Thi</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>Ứng dụng Tạo Đề Thi đang hoạt động!</h2>
            <p>Vui lòng truy cập <a href="/docs">/docs</a> để xem tài liệu API hoặc sử dụng các chức năng của ứng dụng.</p>
        </body>
    </html>
    """
