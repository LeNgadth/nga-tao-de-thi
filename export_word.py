import random
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from database import SessionLocal, CauHoi

def lay_cau_hoi_ngau_nhien(db, mon_hoc, khoi_lop, dang_cau_hoi, muc_do, so_luong):
    """
    Truy vấn ngân hàng câu hỏi và xáo trộn ngẫu nhiên để lấy đủ số lượng yêu cầu.
    """
    ds_cau_hoi = db.query(CauHoi).filter(
        CauHoi.mon_hoc == mon_hoc,
        CauHoi.khoi_lop == khoi_lop,
        CauHoi.dang_cau_hoi == dang_cau_hoi,
        CauHoi.muc_do == muc_do
    ).all()

    if len(ds_cau_hoi) < so_luong:
        print(f"Cảnh báo: Không đủ câu hỏi cho {dang_cau_hoi} - {muc_do} (Cần {so_luong}, hiện có {len(ds_cau_hoi)})")
        return ds_cau_hoi
    
    return random.sample(ds_cau_hoi, so_luong)


def tao_file_word_de_thi(ma_tran_config, output_filename="De_Thi_Chuan.docx"):
    db = SessionLocal()
    doc = Document()

    # Cấu hình font chữ và căn lề tiêu chuẩn
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)

    # Header tiêu đề đề thi
    header = doc.add_paragraph()
    header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = header.add_run(f"ĐỀ KIỂM TRA {ma_tran_config['loai_kiem_tra'].upper()}\n")
    run_title.bold = True
    run_title.font.size = Pt(14)
    
    header.add_run(f"Môn: {ma_tran_config['mon_hoc']} - Khối: {ma_tran_config['khoi_lop']}\n")
    header.add_run(f"Thời gian làm bài: {ma_tran_config['thoi_gian']} phút\n")
    doc.add_paragraph("--------------------------------------------------\n")

    stt_cau = 1

    # --- phần PHẦN I: TRẮC NGHIỆM NHIỀU LỰA CHỌN (DẠNG I) ---
    cau_hoi_d1 = []
    for muc in ['biet', 'hieu', 'vandung']:
        sl = ma_tran_config['ma_tran']['dang_1_nhieu_lua_chon'][muc]
        if sl > 0:
            cau_hoi_d1.extend(lay_cau_hoi_ngau_nhien(db, ma_tran_config['mon_hoc'], ma_tran_config['khoi_lop'], "Dang_I", muc, sl))

    if cau_hoi_d1:
        p_p1 = doc.add_paragraph()
        r_p1 = p_p1.add_run("PHẦN I. Câu hỏi trắc nghiệm nhiều phương án lựa chọn.")
        r_p1.bold = True

        for ch in cau_hoi_d1:
            p = doc.add_paragraph()
            p.add_run(f"Câu {stt_cau}: ").bold = True
            p.add_run(ch.noi_dung)
            
            # In ra các đáp án A, B, C, D
            doc.add_paragraph(f"A. {ch.dap_an_a}\t\tB. {ch.dap_an_b}")
            doc.add_paragraph(f"C. {ch.dap_an_c}\t\tD. {ch.dap_an_d}")
            stt_cau += 1

    # --- PHẦN II: TRẮC NGHIỆM ĐÚNG / SAI (DẠNG II) ---
    cau_hoi_d2 = []
    for muc in ['biet', 'hieu', 'vandung']:
        sl = ma_tran_config['ma_tran']['dang_2_dung_sai'][muc]
        if sl > 0:
            cau_hoi_d2.extend(lay_cau_hoi_ngau_nhien(db, ma_tran_config['mon_hoc'], ma_tran_config['khoi_lop'], "Dang_II", muc, sl))

    if cau_hoi_d2:
        doc.add_paragraph()
        p_p2 = doc.add_paragraph()
        r_p2 = p_p2.add_run("PHẦN II. Câu hỏi trắc nghiệm Đúng/Sai.")
        r_p2.bold = True

        for ch in cau_hoi_d2:
            p = doc.add_paragraph()
            p.add_run(f"Câu {stt_cau}: ").bold = True
            p.add_run(ch.noi_dung + "\n")
            doc.add_paragraph(f"a) {ch.dap_an_a}\nb) {ch.dap_an_b}\nc) {ch.dap_an_c}\nd) {ch.dap_an_d}")
            stt_cau += 1

    # Lưu kết quả ra file
    doc.save(output_filename)
    db.close()
    return output_filename