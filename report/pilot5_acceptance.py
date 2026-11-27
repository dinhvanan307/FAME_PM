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
    first = json.loads((ROOT / "results/pm_results.json").read_text(encoding="utf-8"))["independent_review"]
    p = doc.add_paragraph()
    p.add_run("Vòng K01–K06 (mục 6.6). ").bold = True
    p.add_run(f"Hai người chấm độc lập sáu KPI nghiệp vụ, ghi {first['A']['n'] + first['B']['n']} quyết định. "
              f"A khớp tham chiếu {first['A']['matches']}/{first['A']['n']}, "
              f"B khớp {first['B']['matches']}/{first['B']['n']}.")
    p = doc.add_paragraph()
    p.add_run("Vòng R1–R6 (Phụ lục K). ").bold = True
    p.add_run(f"Tái kiểm sáu hồ sơ kỹ thuật ESG bằng bộ phiếu P1/P2 riêng. Hiện có "
              f"{review['received_complete_ballots']}/2 phiếu hoàn tất và "
              f"{review['valid_decisions']}/{review['expected_decisions']} quyết định hợp lệ. "
              "Phiếu tự chấm của Codex được thống kê riêng.")
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
    p.add_run("Biên bản kỹ thuật lập ngày 25/11/2026. Lịch đề xuất chấm 26/11, đối soát 27/11. "
              "P1 làm A trước, P2 làm B trước. ")
    p.add_run("Chờ đủ hai phiếu để so sánh A/B." if review["comparison"] is None
              else "Xem bảng kết quả hai phiếu độc lập trong phụ lục này. Quyết định cuối chờ PM xét căn cứ và ký.")
    p = doc.add_paragraph(style="Minicap")
    source_link(p, "Bản xuất Zenodo v1", "https://zenodo.org/records/17175084")
    p.add_run("  ·  ")
    source_link(p, "Hồ sơ nghiệm thu và lịch", LINK)
    p.add_run("  ·  D6.4, bảng 43, tr. PDF 70. D6.3, bảng 5, tr. PDF 53.")
    append_codex_review(doc)
    append_weight_evidence(doc)
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


def append_weight_evidence(doc):
    sources = json.loads((ROOT / "results/pilot_portfolio.json").read_text(encoding="utf-8"))["sources"]
    heading(doc, "K  Kiểm chứng năm mức trọng số E/S/G")
    doc.add_paragraph(
        "Ngày 26/11/2026, người viết rà lại R4 và R6. D6.4 yêu cầu ít nhất năm mức phần trăm "
        "cho mỗi chỉ tiêu. D6.3 ghi chức năng hiển thị và điều chỉnh đã có. Kết quả năm mức "
        "ở dòng ngay phía trên thuộc chỉ tiêu tỷ trọng ESG so với lợi nhuận tài chính."
    )
    p = doc.add_paragraph(style="Minicap")
    source_link(p, "D6.4 · bảng 43 · tr. 70", sources["d64"]["url"] + "#page=70")
    p.add_run("   ·   ")
    source_link(p, "D6.3 · bảng 5 · tr. 53", sources["d63"]["url"] + "#page=53")
    t = table(doc, ["Hồ sơ", "Bằng chứng của FAME", "Quyết định của PM học phần"], [2.4, 6.6, 6.4])
    rows = [
        ("R4\nP5-12",
         "Giao diện hiển thị E 55%, S 33%, G 12%. Biểu đồ tròn lặp lại đúng ba tỷ lệ. "
         "Thanh 70% phía trên đo mức ưu tiên ESG so với tài chính.",
         "Giữ mở. Xác nhận được một vector tùy chỉnh cụ thể. Năm lựa chọn định tính trong "
         "bảng hỏi chưa chứng minh năm vector phần trăm đã hiển thị.",
         [("D6.4 · tr. 66", "d64", 66), ("D6.2 · hình 40", "d62", 45)]),
        ("R6\nP5-13",
         "Hình 43 cho chọn trọng số ESG tùy chỉnh, ô đang để trống. Hình 44 ghi danh mục "
         "MS023 ngày 18/09/2025, gồm ABBV.US 15,54% và CVS.US 14,90%.",
         "Giữ mở. Xác nhận bộ tối ưu trả phân bổ theo mã. Còn thiếu chuỗi đầu vào E/S/G và "
         "khuyến nghị ghép được theo từng lượt ở ít nhất năm cấu hình.",
         [("D6.2 · hình 43", "d62", 48), ("Hình 44", "d62", 49)]),
    ]
    for case, observed, decision, references in rows:
        cells = t.add_row().cells
        td(cells[0], case, bold=True)
        p = td(cells[1], observed)
        p.add_run("\n")
        for index, (label, document, page) in enumerate(references):
            if index:
                p.add_run(" · ")
            source_link(p, label, sources[document]["url"] + f"#page={page}")
        td(cells[2], decision)
    doc.add_paragraph(
        "Người viết cũng rà bốn gói mã công khai của marketplace và các khung hình demo. "
        "Các nguồn này chưa cung cấp bộ kiểm thử năm mức. D1.4 xác định KM/JRC vận hành "
        "dịch vụ theo thuê bao. Phép thử 15 cấu hình trên CSV trong bài chỉ đo thay đổi thứ hạng."
    )
    doc.add_paragraph(
        "Bằng chứng cần bổ sung. Với cùng phiên bản, ngày dữ liệu, tập mã và tham số tài chính, "
        "lưu ba trọng số đã chọn, ảnh sau khi áp dụng và danh mục trả về cho từng lượt. "
        "PM có thể đóng R4 ngay khi đủ năm vector hiển thị. R6 cần khuyến nghị gắn được với "
        "từng cấu hình, kể cả khi hai danh mục trùng nhau."
    )
    p = doc.add_paragraph(style="Minicap")
    source_link(p, "D1.4 · bảng 36 · tr. 58",
                "https://www.fame-horizon.eu/wp-content/uploads/2026/02/FAME-D1.4-Data-Management-Plan-II.pdf#page=58")
    p.add_run("   ·   ")
    source_link(p, "Demo từ phút 31:10", "https://www.youtube.com/watch?v=cmfj7OEz2Ow&t=1870s")
    p.add_run("   ·   ")
    source_link(p, "Dấu vết từng nguồn và gói mã", LINK.replace("/tree/", "/blob/") + "/ra_soat_R4_R6.md")


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
