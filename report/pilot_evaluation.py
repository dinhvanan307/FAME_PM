"""Render the linked Pilot 5 decision trail and seven-pilot maturity table."""
from copy import deepcopy

from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from fame_pm.pilot_evaluation import (
    ACCEPTANCE, ZENODO, feedback, page_url, read_evaluation, vi, weight_finding,
)
from report.kpi_appendix import compact, heading, source_link, table, td


def sources(paragraph, references):
    for doc, page in references:
        paragraph.add_run("  ")
        source_link(paragraph, f"D{doc[1]}.{doc[2]} tr. PDF {page}", page_url(doc, page))


def add_pilot_evaluation(doc):
    sections = {p.text.split()[0]: p for p in doc.paragraphs if p.style.name == "Heading 2" and p.text[:1].isdigit()}
    case, next_section = sections["6.2"], sections["6.3"]
    # Replace the two original editorial paragraphs with the sourced case at the same bookmark.
    original = list(case._p.itersiblings())[:2]
    if original[-1].getnext() != next_section._p:
        raise ValueError("Review changed template section 6.2 before replacing its contents")
    for element in original:
        element.getparent().remove(element)
    case.paragraph_format.page_break_before = True
    for row in feedback():
        p = next_section.insert_paragraph_before()
        p.add_run(row["title"] + ". ").bold = True
        p.add_run(row["text"])
        sources(p, row["sources"])
    p = next_section.insert_paragraph_before()
    p.add_run("Phép kiểm của người viết. ").bold = True
    p.add_run(weight_finding() + " ")
    source_link(p, "Dữ liệu Zenodo v1", ZENODO)
    p = next_section.insert_paragraph_before()
    p.add_run("Quyết định nghiệm thu của người viết. ").bold = True
    p.add_run(ACCEPTANCE)
    sources(p, [("d64", 70)])

    p = sections["7.2"].insert_paragraph_before()
    p.add_run("Mức trưởng thành theo Innovation Pentagon. ").bold = True
    p.add_run("Người viết tổng hợp bảy hình tự đánh giá ở Phụ lục J. Trung bình bảy pilot khớp "
              "giá trị FAME công bố trên cả năm chiều. Pilot 5 tự chấm tuân thủ 4,60/5. Để chốt "
              "P5-08 vẫn cần đếm số danh mục đạt chuẩn trên tổng số danh mục được kiểm tra.")
    sources(p, [("d63", 51), ("d63", 52), ("d63", 82)])

    data, means = read_evaluation()
    heading(doc, "J  Điểm Innovation Pentagon của bảy pilot")
    p = doc.add_paragraph("FAME thu bảng hỏi pha 1 theo thang 1–5 và tổng hợp theo năm chiều. "
                          "Bộ Excel gồm bốn phần về kỹ thuật, kinh doanh, bảng hỏi Pentagon và hội thảo. "
                          "Khi đánh giá toàn dự án, FAME kết hợp bảng điểm này với KPI trước/sau và ý kiến các bên liên quan.")
    sources(p, [("d63", 11), ("d63", 12), ("d63", 76)])
    caption_text = "Điểm do FAME công bố và trung bình do người viết tính lại"
    caption = doc.add_paragraph(f"Bảng J.1. {caption_text}", style="Caption")
    # Match the existing list of tables, including its clickable page-reference field.
    anchor = "pentagon_scores"
    bookmark_id = str(1 + max(int(x.get(qn("w:id"))) for x in doc.element.xpath(".//w:bookmarkStart")))
    start = OxmlElement("w:bookmarkStart")
    start.set(qn("w:name"), anchor)
    start.set(qn("w:id"), bookmark_id)
    end = OxmlElement("w:bookmarkEnd")
    end.set(qn("w:id"), bookmark_id)
    caption.runs[0]._r.addprevious(start)
    caption._p.append(end)
    prior = next(p for p in doc.paragraphs if p.style.name == "Index" and p.text.startswith("Bảng B.1"))
    entry = deepcopy(prior._p)
    link = entry.xpath("./w:hyperlink")[0]
    link.set(qn("w:anchor"), anchor)
    link.xpath(".//w:t")[0].text = "Bảng J.1   " + caption_text
    entry.xpath(".//w:instrText")[0].text = f" PAGEREF {anchor} \\h "
    prior._p.addnext(entry)
    t = table(doc, ["Pilot", "Thị trường", "Khách hàng", "Tuân thủ", "Nguồn lực", "Công nghệ", "D6.3 · trang PDF"],
              [2.3, 2.05, 2.0, 1.85, 1.85, 1.95, 2.95])
    for row in [*data["pilots"], data["portfolio"], {"scores": means}]:
        cells = t.add_row().cells
        pilot = row.get("pilot")
        name = str(pilot) if pilot else ("FAME" if "figure" in row else "Tính lại")
        td(cells[0], name, bold=not pilot)
        for i, value in enumerate(row["scores"], 1):
            td(cells[i], vi(value), bold=not pilot)
        if "figure" in row:
            source_link(compact(cells[-1].paragraphs[0]), f"Hình {row['figure']} · tr. {row['page']}",
                        page_url("d63", row["page"]))
        else:
            td(cells[-1], "TB bảy pilot")
    p = doc.add_paragraph()
    p.add_run("Cách tính của người viết. ").bold = True
    p.add_run("Mỗi pilot có trọng số bằng nhau. Với mỗi chiều, cộng bảy nhãn số in trong hình, chia bảy "
              "rồi làm tròn đến hai chữ số thập phân. Kết quả khớp Hình 16 ở cả năm chiều. "
              "Chưa có phiếu từng người, cỡ mẫu theo câu và quy tắc xử lý phiếu thiếu để tính lại từ cấp người trả lời.")
    p = doc.add_paragraph()
    p.add_run("Hàm ý quản lý. ").bold = True
    p.add_run("Pilot 4 có điểm thị trường 4,17 và công nghệ 2,33. Người viết đề xuất kiểm tra vận hành "
              "và tích hợp trước quyết định nhân rộng. Điểm tuân thủ trải từ 1,00 ở Pilot 6 đến 5,00 ở Pilot 7. "
              "Vì vậy, cần rà hồ sơ tuân thủ từng pilot trước khi quyết định chấp nhận rủi ro. Mục 6.2 minh họa "
              "cách dùng phản hồi của người dùng để đặt điều kiện nghiệm thu ở Pilot 5.")
    p = compact(doc.add_paragraph())
    source_link(p, "Bảng điểm, bằng chứng và mã đối chiếu trên GitHub",
                "https://github.com/dinhvanan307/FAME_PM/blob/main/docs/innovation-pentagon.md")
