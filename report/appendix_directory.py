"""Build an internal A–L evidence index using the report's real appendix headings."""

import re

from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

from report.kpi_appendix import table, td

QUESTIONS = {
    "A": "Bên nào chịu trách nhiệm cho từng sản phẩm?",
    "B": "Ngày bàn giao và tỷ trọng tài trợ được tính thế nào?",
    "C": "Cần đo gì trước khi quyết định mở rộng Pilot 5?",
    "D": "Chạy lại phép kiểm dữ liệu ESG ban đầu thế nào?",
    "E": "Thành phần top 5 đổi ra sao khi đổi trọng số ESG?",
    "F": "Bảy pilot đã bàn giao gì và FAME công bố kết quả nào?",
    "G": "Mục tiêu, kỳ đo và bằng chứng của từng KPI ở đâu?",
    "H": "Vì sao hai trong 25 hồ sơ được chốt khi rà thêm nguồn?",
    "I": "Trong 23 hồ sơ còn mở, kiểm được gì bằng mã gốc?",
    "J": "FAME chấm năm chiều đổi mới của từng pilot ra sao?",
    "K": "Pilot 5 đã kiểm được gì về 100 mã, trọng số và tín hiệu có ngày?",
    "L": "Hạn, ngày giao, phiên bản và bìa nguồn của từng báo cáo ở đâu?",
}


def add_appendix_directory(doc):
    landing = next(
        p for p in doc.paragraphs if p.style.name == "FrontHead" and p.text == "Phụ lục"
    )
    headings = {}
    for p in doc.paragraphs:
        if p.style.name == "Heading 2":
            match = re.match(r"^(?:Phụ lục )?([A-L])(?:  |\. )", p.text)
            if match:
                headings.setdefault(match[1], p)
    if headings.keys() != QUESTIONS.keys():
        raise ValueError("Appendix headings do not match the A–L evidence index")

    index = table(doc, ["Câu hỏi cần đối chiếu", "Mở hồ sơ"], [12.2, 3.6])
    landing._p.addnext(index._tbl)
    next_id = 1 + max(
        int(el.get(qn("w:id"))) for el in doc.element.xpath(".//w:bookmarkStart")
    )
    for offset, (letter, question) in enumerate(QUESTIONS.items()):
        anchor = "FameAppendix" + letter
        bookmark_id = str(next_id + offset)
        start = OxmlElement("w:bookmarkStart")
        start.set(qn("w:id"), bookmark_id)
        start.set(qn("w:name"), anchor)
        end = OxmlElement("w:bookmarkEnd")
        end.set(qn("w:id"), bookmark_id)
        target = headings[letter]
        target.runs[0]._r.addprevious(start)
        target._p.append(end)

        cells = index.add_row().cells
        td(cells[0], question)
        p = td(cells[1], "")
        link = OxmlElement("w:hyperlink")
        link.set(qn("w:anchor"), anchor)
        run = p.add_run("Phụ lục " + letter)
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor.from_string("24526D")
        run.underline = True
        link.append(run._r)
        p._p.append(link)
    headings["A"].paragraph_format.page_break_before = True
