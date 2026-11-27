"""Add the portfolio acceptance register to the existing Vietnamese course report."""

from collections import Counter
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.shared import Cm, Pt, RGBColor

from fame_pm.kpi_matrix import STATUSES, read_matrix

PILOTS = [
    "FaMLy",
    "Ví công dân Athens",
    "Thanh toán và phòng chống rửa tiền",
    "Hồ sơ tài trợ EU",
    "Xếp hạng ESG và danh mục",
    "Bảo hiểm khí hậu",
    "Dữ liệu công nghiệp",
]
SPEC_TABLES = (11, 25, 31, 35, 43, 49, 56)


def source_link(paragraph, label, url):
    link = OxmlElement("w:hyperlink")
    link.set(
        qn("r:id"),
        paragraph.part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True),
    )
    run = paragraph.add_run(label)
    run.font.underline = True
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor.from_string("24526D")
    link.append(run._r)
    paragraph._p.append(link)


def compact(p):
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    f = p.paragraph_format
    f.first_line_indent = Cm(0)
    f.space_before = Pt(0)
    f.space_after = Pt(3)
    f.line_spacing = 1.08
    return p


def td(cell, text, *, bold=False, second=False):
    p = compact(cell.add_paragraph() if second else cell.paragraphs[0])
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(10.5)
    return p


def table(doc, headings, widths):
    t = doc.add_table(rows=1, cols=len(headings))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for col, cell, label, width in zip(t.columns, t.rows[0].cells, headings, widths):
        col.width = Cm(width)
        cell.width = Cm(width)
        td(cell, label, bold=True)
        fill = OxmlElement("w:shd")
        fill.set(qn("w:fill"), "E5EEF1")
        cell._tc.get_or_add_tcPr().append(fill)
    t.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
    return t


def heading(doc, title):
    p = doc.add_paragraph(title, style="Heading 2")
    p.paragraph_format.page_break_before = True


def append_register(doc):
    rows = read_matrix()
    counts = Counter(r["assessment"] for r in rows)
    summary = (
        f"Đối chiếu toàn dự án. Trong {len(rows)} KPI của bảy pilot, người viết xếp "
        f"{counts[STATUSES[0]]} đạt, {counts[STATUSES[1]]} không đạt, "
        f"{counts[STATUSES[2]]} thiếu bằng chứng và {counts[STATUSES[3]]} không áp dụng theo FAME. "
        "Phụ lục G ghi từng chỉ tiêu. Phụ lục H giải thích vì sao 2 trong 25 hồ sơ đã được đóng sau khi đối chiếu thêm nguồn. Phụ lục I trình bày phép thử trên 23 hồ sơ còn mở và dữ liệu cần bổ sung."
    )
    conclusion = next(
        p for p in doc.paragraphs if p.text.startswith("Kết quả so sánh quản lý.")
    )
    paragraph = doc.add_paragraph(summary)
    conclusion._p.addnext(paragraph._p)
    heading(doc, "G  Ma trận nghiệm thu theo 65 KPI")
    doc.add_paragraph(
        "Người viết đối chiếu từng dòng trong bảy bảng chỉ tiêu của D6.4 với các bảng 1–7 "
        "của D6.3. Mục tiêu và kết quả là thông tin do dự án công bố. Quyết định nghiệm thu "
        "phản ánh đánh giá hồi cứu của người viết ở mức bằng chứng công khai."
    )
    t = table(
        doc,
        ["Pilot", "KPI", "Đạt", "Không đạt", "Thiếu bằng chứng", "Không áp dụng¹"],
        [2.6, 1.3, 2.0, 2.4, 3.4, 3.4],
    )
    for i in range(1, 9):
        sample = rows if i == 8 else [r for r in rows if int(r["pilot"]) == i]
        totals = Counter(r["assessment"] for r in sample)
        for cell, value in zip(
            t.add_row().cells,
            ["Tổng" if i == 8 else str(i), len(sample), *(totals[s] for s in STATUSES)],
        ):
            td(cell, str(value), bold=i == 8)
    doc.add_paragraph(
        "¹ Pilot 1 chưa đưa dữ liệu bên ngoài vào mô hình nên FAME ghi không áp dụng cho "
        "phép thử tăng ROC-AUC. Hồ sơ công khai chưa ghi nhận việc miễn trừ yêu cầu."
    )
    doc.add_paragraph(
        "Mục tiêu nhiều điều kiện chỉ đóng khi có bằng chứng đủ các điều kiện. "
        "Chỉ tiêu có số đo dưới ngưỡng hoặc được FAME ghi rõ dưới ngưỡng được xếp không đạt. "
        "Ô NA hoặc nhận xét định tính về một ngưỡng số được giữ mở. Tháng của pha đánh giá "
        "và ngày thu thập quan sát riêng được phân biệt ở đầu từng bảng."
    )
    doc.add_paragraph(
        "Ví dụ về thay đổi mục tiêu. D6.4 yêu cầu nhập đủ 100% bản ghi theo từng bộ dữ liệu "
        "của Pilot 4. D6.3 đổi sang đếm hơn 20 bản ghi và báo cáo 33. Kết luận đối với yêu cầu "
        "gốc cần mẫu số của từng nguồn hoặc hồ sơ phê duyệt thay đổi. Xem P4-02."
    )
    p = compact(doc.add_paragraph())
    source_link(
        p,
        "Mở ma trận Excel với bộ lọc và liên kết gốc",
        "https://github.com/dinhvanan307/FAME_PM/blob/main/FAME_Ma_tran_65_KPI.xlsx",
    )
    for i, name in enumerate(PILOTS, 1):
        sample = [r for r in rows if int(r["pilot"]) == i]
        block_size = 4 if i == 3 else 5
        for j in range(0, len(sample), block_size):
            block = sample[j : j + block_size]
            heading(doc, f"Pilot {i} · {name}")
            p = compact(doc.add_paragraph())
            p.add_run(f"{block[0]['id']} đến {block[-1]['id']}   ·   ").bold = True
            p.add_run(block[0]["period"] + " ")
            source_link(p, "Nguồn kỳ đánh giá", block[0]["period_url"])
            t = table(
                doc,
                [
                    "Chỉ tiêu và nguồn PDF",
                    "Mục tiêu và kết quả FAME",
                    "Nghiệm thu của người viết",
                ],
                [3.8, 6.35, 5.0],
            )
            for r in block:
                tr = t.add_row()
                tr._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
                key, measurement, decision = tr.cells
                td(key, r["id"] + " · " + r["kpi"], bold=True)
                if r["legacy_id"]:
                    td(key, "Phiếu 6 KPI · " + r["legacy_id"], second=True)
                for label, url in [
                    (
                        f"D6.4 bảng {SPEC_TABLES[i - 1]} · tr. {r['target_pages']}",
                        r["target_url"],
                    ),
                    (f"D6.3 bảng {i} · tr. {r['actual_pages']}", r["actual_url"]),
                ]:
                    source_link(compact(key.add_paragraph()), label, url)
                if r["supporting_url"]:
                    source_link(
                        compact(key.add_paragraph()),
                        "D6.2 · tr. " + r["supporting_url"].split("=")[-1],
                        r["supporting_url"],
                    )
                td(measurement, "Mục tiêu. " + r["target"])
                td(measurement, "Kết quả. " + r["actual"], second=True)
                td(decision, r["assessment"], bold=True)
                td(decision, r["rationale"], second=True)

    append_review(doc, rows)
    append_execution(doc, rows)


def append_review(doc, rows):
    reviewed = sorted(
        (r for r in rows if r["review"]), key=lambda r: r["review"]["order"]
    )
    closed = [r for r in reviewed if r["assessment"] != r["review"]["before"]]
    heading(doc, "H  Rà soát bằng chứng cho 25 KPI còn mở")
    doc.add_paragraph(
        f"Lần rà ngày 23/11/2026 lấy phiên bản 6c929ea của ma trận làm mốc. "
        f"Trong {len(reviewed)} hồ sơ đang mở, người viết đổi kết luận của {len(closed)} KPI "
        f"và giữ mở {len(reviewed) - len(closed)} KPI. Phần G ghi kết luận hiện hành cho toàn bộ dự án. "
        "Các trang dưới đây ghi từng bằng chứng mới và điều kiện cần để quyết định."
    )
    doc.add_paragraph(
        "Hai quyết định thay đổi thuộc Pilot 5. Trong cùng bảng 5 của D6.3, trang 52 ghi "
        "28 người xem và 25 người dùng chức năng so sánh. Trang 53 ghi 9 bảng khuyến nghị "
        "ESG đã so sánh. D1.4 định danh chín bảng này theo nhóm tích cực, cân bằng và thận trọng "
        "ở các bảng 27–35. Chín bộ trọng số danh mục được báo cáo ở một dòng riêng."
    )
    p = compact(doc.add_paragraph())
    example = next(r for r in reviewed if r["id"] == "P5-05")
    for label, url in [
        ("D6.3 · tr. 52", example["actual_url"]),
        *((s["label"], s["url"]) for s in example["review"]["sources"]),
    ]:
        source_link(p, label, url)
        p.add_run("   ")
    doc.add_paragraph(
        "Quy tắc của người viết. Đặc tả đặt hai ngưỡng tổng ở cấp pilot. Hồ sơ được đóng khi "
        "có số người và số bảng cùng loại thực sự dùng trong cùng kỳ, kể cả khi dự án ghi chúng "
        "ở hai dòng khác nhau. Dữ liệu công bố chỉ cho kết luận về cả nhóm. Muốn biết từng người "
        "đã xem bao nhiêu bảng, cần nhật ký có mã người dùng và mã bảng."
    )
    doc.add_paragraph(
        "Pilot 3 có sơ đồ, nguyên mẫu trực tuyến và triển khai AWS. Số endpoint trong mã chung, "
        "số khách mời hội nghị và số bản ghi trong bộ dữ liệu đều có thể đếm được, nhưng mỗi đại "
        "lượng trả lời một câu hỏi khác. Với chỉ tiêu đo sử dụng hoặc kiểm thử, người viết tìm "
        "bản ghi của đúng pilot, đúng thao tác và đúng kỳ."
    )
    p = compact(doc.add_paragraph())
    source_link(
        p,
        "Quản lý dữ liệu đánh giá WP6 · D1.4, tr. 33",
        example["review"]["sources"][1]["url"].split("#")[0] + "#page=33",
    )
    doc.add_paragraph(
        "Ý nghĩa quản lý. Tỷ lệ hồ sơ cũ được chốt là 2/25 (8%) theo tính toán của người viết. "
        "Con số này đo mức hoàn thiện hồ sơ nghiệm thu. Phép rà tài liệu không đo biến động hiệu suất của FAME. "
        "Để đóng các dòng còn lại, nhóm nghiệm thu có thể chuyển yêu cầu ở cột cuối cho bên phụ trách "
        "pilot và chỉ cập nhật khi nhận được bằng chứng cùng phạm vi."
    )
    for pilot in (3, 5, 2, 4, 7):
        group = [r for r in reviewed if int(r["pilot"]) == pilot]
        for start in range(0, len(group), 4):
            page = group[start : start + 4]
            heading(doc, f"H · Pilot {pilot} · {PILOTS[pilot - 1]}")
            p = compact(doc.add_paragraph())
            ids = ", ".join(r["id"] for r in page)
            p.add_run(f"{ids}   ·   Trước rà: Thiếu bằng chứng").bold = True
            t = table(
                doc,
                [
                    "KPI và nguồn đối chiếu",
                    "Bằng chứng tìm thấy",
                    "Kết luận của người viết",
                ],
                [4.0, 5.7, 5.55],
            )
            for r in page:
                row = t.add_row()
                row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
                code, finding, decision = row.cells
                td(code, r["id"] + " · " + r["kpi"], bold=True)
                for source in r["review"]["sources"]:
                    source_link(
                        compact(code.add_paragraph()), source["label"], source["url"]
                    )
                td(finding, r["review"]["finding"])
                td(decision, r["assessment"], bold=True)
                td(decision, r["review"]["resolution"], second=True)


def append_execution(doc, rows):
    from fame_pm.open23_register import published

    cases = sorted(
        (r for r in rows if r.get("execution")), key=lambda r: r["execution"]["order"]
    )
    snapshot = published()
    fifth = snapshot["pilot5"]
    profiles = fifth["weights"]["profiles"]
    heading(doc, "I  Kiểm thử bằng dữ liệu và mã công khai")
    doc.add_paragraph(
        "Đợt kiểm thử lấy 23 hồ sơ đang mở ở commit 2ee5042 làm mốc. Với từng hồ sơ, "
        "người viết xác định có thể đo trực tiếp thao tác nào, dùng mã của ai và còn thiếu đầu vào gì. "
        "Không hồ sơ nào thu được đủ các vế để đổi quyết định nghiệm thu. Các trang sau ghi kết quả "
        "và yêu cầu dữ liệu cho từng mã. Tên bên giữ hồ sơ là đề xuất của người viết."
    )
    doc.add_paragraph(
        "Pilot 3. Người viết chạy hàm searchAssets từ gói FDAC gốc với ba ví dụ do FAME cung cấp. "
        "Cả ba giữ nguyên nội dung truy vấn và trả được phản hồi thử. Tầng truyền dữ liệu dùng mẫu "
        "trong bộ nhớ. Phép thử xác nhận cách hoạt động của mã máy khách. Muốn xét ngưỡng vận hành "
        "của Pilot 3, cần đếm các sự kiện thực tế theo loại và kỳ."
    )
    doc.add_paragraph(
        "Pilot 5. Trên 604 dòng và 100 mã của bản Zenodo v1, người viết lần lượt thay trọng số của "
        "một trụ và chia đều phần còn lại cho hai trụ kia. Mỗi tổ hợp được so với trọng số ba trụ "
        "bằng nhau trên cùng dòng. Bảng ghi số dòng thay đổi ít nhất một mã trong top 5. "
        "Điểm bằng nhau được xếp theo mã cổ phiếu tăng dần."
    )
    t = table(
        doc, ["Trọng số của trụ", "Thay E", "Thay S", "Thay G"], [4.8, 3.45, 3.45, 3.45]
    )
    for pc in (0, 25, 50, 75, 100):
        selected = [
            p["rows_changing_top5_members_vs_equal"]
            for p in profiles
            if p["weight_percent"] == pc
        ]
        for cell, value in zip(t.add_row().cells, [f"{pc}%", *selected]):
            td(cell, str(value))
    doc.add_paragraph(
        f"15 cấu hình × 604 dòng cho 9.060 bảng xếp hạng. Dữ liệu có {fifth['weights']['unique_input_panels']} "
        "bộ điểm E/S/G phân biệt khi so toàn bộ 100 mã. Các dòng lặp được giữ đúng số lần trong bản xuất. "
        "Phép thử này dùng mã của người viết để tính điểm trên dữ liệu FAME. Nghiệm thu giao diện và "
        "bộ tối ưu vẫn cần thử cùng các cấu hình trên bản Pilot 5 đã bàn giao."
    )
    p = compact(doc.add_paragraph())
    source_link(
        p,
        "Mã chạy và kết quả chi tiết trên GitHub",
        "https://github.com/dinhvanan307/FAME_PM/blob/main/results/open23_runs.json",
    )
    for start in range(0, len(cases), 3):
        subset = cases[start : start + 3]
        heading(doc, "I · Hồ sơ kiểm thử " + ", ".join(r["id"] for r in subset))
        t = table(
            doc,
            ["KPI và cách kiểm", "Phép đo và giới hạn", "Hồ sơ cần bổ sung"],
            [3.6, 5.5, 6.15],
        )
        for r in subset:
            c = r["execution"]
            row = t.add_row()
            row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
            key, observed, missing = row.cells
            td(key, r["id"] + " · " + r["kpi"], bold=True)
            td(key, c["method"], second=True)
            source_link(compact(key.add_paragraph()), "Nguồn đối chiếu", c["url"])
            source_link(compact(key.add_paragraph()), "Mục tiêu D6.4", r["target_url"])
            td(observed, c["observation"])
            td(missing, c["owner"], bold=True)
            td(missing, c["request"], second=True)
            td(missing, c["decision_rule"], second=True)
