"""Append the evidence and PM disposition of the November Pilot 5 acceptance round."""
import json
from pathlib import Path

from openpyxl import load_workbook
from Pilot5_nghiem_thu.tong_hop import DECISIONS, SPEC
from report.kpi_appendix import heading, source_link, table, td

ROOT = Path(__file__).resolve().parents[1]
LINK = "https://github.com/dinhvanan307/FAME_PM/tree/main/Pilot5_nghiem_thu"


def append_acceptance(doc, review):
    data = json.loads((ROOT / "Pilot5_nghiem_thu/phep_do.json").read_text(encoding="utf-8"))
    d = lambda n: f"{n:,}".replace(",", ".")
    rows = data["exceptions"]
    heading(doc, "K  Biên bản tái kiểm điểm ESG của Pilot 5")
    doc.add_paragraph("Ngày 25/11/2026, PM học phần lập biên bản kỹ thuật cho bản xuất Zenodo v1 "
                      "trước khi thu phiếu chấm. Căn cứ nghiệm thu là độ khớp với các giá trị do tác giả công bố.")
    p = doc.add_paragraph()
    p.add_run("Dữ liệu và tiêu chí. ").bold = True
    p.add_run(f"Đã kiểm dung lượng và MD5 của {len(data['files'])} CSV. Dòng 1 dùng hiệu chuẩn. "
              f"Trên 603 dòng tiếp theo, ngưỡng từng ô là 10⁻⁸ điểm. Người viết đã biết kết quả "
              "thăm dò lúc khóa tiêu chí ở commit 7ac10f3. Lượt xác nhận dùng lại cùng bản phát hành.")
    p = doc.add_paragraph()
    p.add_run("Thay đổi được kiểm soát. ").bold = True
    p.add_run(f"Lần đầu ghép được {data['tickers'] - len(rows)} mã với một ngành. Lượt sau kiểm đủ "
              f"{data['tickers']} mã bằng cách dùng trung bình tám ngành theo từng dòng cho chín mã còn lại. "
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
    p.add_run("P1 làm lượt thường (A) trước, P2 làm lượt có checklist (B) trước. Lịch đề xuất chấm "
              "26/11 và đối soát 27/11. ")
    p.add_run(f"Khi dựng báo cáo có {review['received_complete_ballots']}/2 phiếu hoàn tất "
              f"và {review['valid_decisions']}/{review['expected_decisions']} quyết định hợp lệ. ")
    p.add_run("Chờ đủ hai phiếu để so sánh A/B." if review["comparison"] is None
              else "Xem bảng kết quả hai phiếu độc lập trong phụ lục này. Quyết định cuối chờ PM xét căn cứ và ký.")
    p = doc.add_paragraph(style="Minicap")
    source_link(p, "Bản xuất Zenodo v1", "https://zenodo.org/records/17175084")
    p.add_run("  ·  ")
    source_link(p, "Hồ sơ nghiệm thu và lịch", LINK)
    p.add_run("  ·  D6.4, bảng 43, tr. PDF 70. D6.3, bảng 5, tr. PDF 53.")
    append_codex_review(doc)
    if review["comparison"] is not None:
        append_review_comparison(doc, review)


def append_codex_review(doc):
    filename = "Tu_cham_Codex.xlsx"
    book = load_workbook(ROOT / "Pilot5_nghiem_thu" / filename, data_only=True, read_only=True)
    records = {}
    try:
        if book["Huong dan"]["A1"].value != "Pilot 5    |    Phiếu tự chấm Codex":
            raise ValueError("Phiếu tự chấm sai tên người đánh giá")
        for i, (_, ids) in enumerate(SPEC["P1"], 1):
            sheet = book[f"Luot {i}"]
            for key, row in zip(ids, sheet.iter_rows(min_row=6, max_row=8, values_only=True)):
                case, title, _, _, start, end, seconds, decision, reason = row[:9]
                if (case != key or decision not in DECISIONS or not reason
                        or seconds != (end - start).total_seconds() or seconds < 1):
                    raise ValueError(f"Phiếu tự chấm có dòng không hợp lệ: {key}")
                records[case] = (title, decision, seconds, reason)
    finally:
        book.close()
    if records.keys() != SPEC["cases"].keys():
        raise ValueError("Phiếu tự chấm thiếu hồ sơ")
    accepted = sum(values[1] == "Duyệt" for values in records.values())
    heading(doc, "K  Phiếu tự chấm của Codex")
    doc.add_paragraph(f"Ngày 26/11/2026, Codex duyệt {accepted}/{len(records)} hồ sơ sau khi chạy lại "
                      "phép kiểm trên 12 CSV và đối chiếu đặc tả với báo cáo đánh giá của FAME. "
                      "Codex đã biết kết quả kỹ thuật của lượt trước. Thời gian dưới đây tính từ lúc "
                      "mở hồ sơ đến lúc chốt trên biểu mẫu, gồm cả thời gian chạy công cụ.")
    t = table(doc, ["Hồ sơ", "Quyết định", "Giây", "Căn cứ đối chiếu"], [3.0, 2.0, 1.2, 9.2])
    for case in sorted(records):
        title, decision, seconds, reason = records[case]
        for cell, text in zip(t.add_row().cells, (case + " · " + title, decision, str(seconds), reason)):
            td(cell, text)
    doc.add_paragraph("Đây là một lượt tự kiểm. PM chỉ tính mức đồng thuận và so sánh hiệu quả checklist "
                      "khi nhận đủ hai phiếu chấm độc lập P1 và P2.")
    p = doc.add_paragraph(style="Minicap")
    source_link(p, "Phiếu Excel có giờ và căn cứ từng hồ sơ", LINK.replace("/tree/", "/blob/") + "/" + filename)


def append_review_comparison(doc, review):
    heading(doc, "K  Kết quả hai phiếu chấm độc lập")
    doc.add_paragraph("Mỗi hồ sơ R1–R6 được chấm một lần ở mỗi điều kiện. "
                      "Quyết định được đối chiếu với tiêu chí đã khóa. Thời gian tính từ lúc "
                      "bắt đầu đọc hồ sơ đến khi ghi xong quyết định và căn cứ.")
    metrics = review["comparison"]
    t = table(doc, ["Chỉ số", "A · Thông thường", "B · Có checklist"], [7.0, 4.2, 4.2])
    for title, key, denominator in [
        ("Quyết định đúng / số quyết định", "correct", "cases"),
        ("Duyệt nhầm / hồ sơ cần từ chối", "false_approvals", "reference_negative"),
        ("Từ chối nhầm / hồ sơ đủ căn cứ", "false_rejections", "reference_positive"),
        ("Thời gian trung bình (giây/hồ sơ)", "mean_seconds", None),
        ("Thời gian trung vị (giây/hồ sơ)", "median_seconds", None),
    ]:
        cells = t.add_row().cells
        td(cells[0], title)
        for cell, condition in zip(cells[1:], ("A", "B")):
            m = metrics[condition]
            value = f"{m[key]}/{m[denominator]}" if denominator else f"{m[key]:.2f}".replace(".", ",")
            td(cell, value)
    conflicts = review["disagreement_ids"]
    pairs = review["agreements"] + len(conflicts)
    p = doc.add_paragraph(f"Hai người đồng thuận ở {review['agreements']}/{pairs} hồ sơ. ")
    if conflicts:
        p.add_run("PM cần đối soát căn cứ cho các hồ sơ " + ", ".join(conflicts) + ". ")
    p.add_run("PM xét các căn cứ trước khi ký. Các thống kê mô tả hai người và sáu hồ sơ của vòng P5-V1.")
