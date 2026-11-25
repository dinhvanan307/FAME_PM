"""Append the evidence and PM disposition of the November Pilot 5 acceptance round."""
import json
from pathlib import Path

from report.kpi_appendix import heading, source_link, table, td

ROOT = Path(__file__).resolve().parents[1]
LINK = "https://github.com/dinhvanan307/FAME_PM/tree/main/Pilot5_nghiem_thu"


def append_acceptance(doc):
    data = json.loads((ROOT / "Pilot5_nghiem_thu/phep_do.json").read_text(encoding="utf-8"))
    d = lambda n: f"{n:,}".replace(",", ".")
    rows = data["exceptions"]
    heading(doc, "K  Biên bản tái kiểm điểm ESG của Pilot 5")
    doc.add_paragraph("Ngày 25/11/2026 • PM học phần • Bản xuất Zenodo v1. "
                      "Quyết định kỹ thuật dựa trên độ khớp với số liệu do tác giả công bố. "
                      "Hai phiếu độc lập và quyết định ký của PM thuộc bước tiếp theo.")
    p = doc.add_paragraph()
    p.add_run("Dữ liệu và tiêu chí. ").bold = True
    p.add_run(f"Đã kiểm dung lượng và MD5 của {len(data['files'])} CSV. Dòng 1 dùng hiệu chuẩn. "
              f"Trên 603 dòng tiếp theo, ngưỡng từng ô là 10⁻⁸ điểm. Người viết đã biết kết quả "
              "thăm dò lúc khóa tiêu chí ở commit 7ac10f3. Lượt xác nhận dùng lại cùng bản phát hành.")
    p = doc.add_paragraph()
    p.add_run("Thay đổi được kiểm soát. ").bold = True
    p.add_run("Giữ cách ghép một ngành ở 91 mã. Với chín mã còn lại, thay bằng trung bình cộng "
              "của tám chuỗi ngành trên từng dòng. Giữ cùng bản dữ liệu, mẫu số và dung sai. "
              f"Số ô được tái tạo đúng tăng từ {d(data['baseline_matched'])} lên {d(data['matched'])} "
              f"trên {d(data['denominator'])} ô E/S/G, tương ứng 91% lên 100%. "
              f"Sai số tuyệt đối lớn nhất {data['max_abs_pillar_error']} điểm.")
    tab = table(doc, ["Mã ngoại lệ", "Trụ E/S/G khớp trên 1.809", "Tổng điều chỉnh khớp trên 603",
                      "Giữ tham chiếu cố định, trên 1.809"], [3.2,4.0,4.1,4.1])
    for r in rows:
        for cell, value in zip(tab.add_row().cells,(r["ticker"],d(r["adjusted_pillars_matched"]),
                              d(r["adjusted_total_matched"]),d(r["frozen_reference_matched"]))):
            td(cell, value)
    p = doc.add_paragraph()
    p.add_run("Quyết định và giới hạn. ").bold = True
    p.add_run("Đóng chín ngoại lệ về tái tạo số học trên v1. P5-12 cần bằng chứng giao diện ở ít nhất "
              "năm mức. P5-13 cần đầu vào, trọng số và đầu ra của bộ tối ưu trên các mức đã chọn. "
              "Lợi suất MS020 còn thiếu lịch giao dịch và cấu hình chạy tương ứng.")
    p = doc.add_paragraph()
    p.add_run("Kiểm soát tiến độ và chất lượng. ").bold = True
    p.add_run("Hai người chấm sáu hồ sơ theo thứ tự A/B đảo chiều. Lịch đề xuất chấm 26/11 và đối soát "
              "27/11. Tại thời điểm lập biên bản có 0/2 phiếu và 0/12 quyết định. PM chờ đủ hai phiếu để "
              "tính số duyệt nhầm, từ chối nhầm, thời gian và mức đồng thuận trước khi ký.")
    p = doc.add_paragraph(style="Minicap")
    source_link(p, "Bản xuất Zenodo v1", "https://zenodo.org/records/17175084")
    p.add_run("  ·  ")
    source_link(p, "Hồ sơ nghiệm thu và lịch", LINK)
    p.add_run("  ·  D6.4, bảng 43, tr. PDF 70. D6.3, bảng 5, tr. PDF 53.")
