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
        "Phụ lục G ghi mục tiêu, kết quả, kỳ đánh giá và trang nguồn cho từng chỉ tiêu."
    )
    conclusion = next(
        p for p in doc.paragraphs if p.text.startswith("Kết quả so sánh quản lý.")
    )
    conclusion.add_run(" " + summary)
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
