"""Render the complete cover-date register from the checked schedule results."""

from datetime import date

from report.kpi_appendix import heading, source_link, table, td


def printed_date(value):
    return date.fromisoformat(value).strftime("%d/%m/%Y")


def append_schedule(doc, schedule):
    records = schedule["deliverables"]
    sources = {r["deliverable"]: r["source_url"].split("#")[0] for r in records}
    for index in range(0, len(records), 16):
        heading(
            doc,
            "Phụ lục L. Sổ bàn giao 32 báo cáo FAME"
            if index == 0
            else "Phụ lục L (tiếp). Ngày giao và các ngoại lệ",
        )
        if index == 0:
            p = doc.add_paragraph(
                "Nguồn FAME. Mỗi dòng ghi phiên bản, tháng đến hạn (M), Due Date và Delivered Date trên cùng một bìa PDF. Bấm vào mã sản phẩm để mở trang 1. "
            )
            source_link(
                p,
                "Danh mục công bố của FAME",
                "https://www.fame-horizon.eu/deliverables-download/",
            )
            doc.add_paragraph(
                "Phép tính của người viết. Lấy ngày giao trừ hạn ghi ngày trên bìa, tính cả cuối tuần và ngày lễ. Số dương là trễ, số âm là sớm, số 0 là đúng ngày. Đơn vị quan sát là phiên bản công khai của từng sản phẩm."
            )
        t = table(
            doc,
            ("Bìa PDF", "Bản", "Tháng", "Hạn trên bìa", "Ngày giao", "Lệch (ngày)"),
            (2.7, 1.7, 1.8, 3.3, 3.3, 2.8),
        )
        for row in records[index : index + 16]:
            cells = t.add_row().cells
            source_link(td(cells[0], ""), row["deliverable"], row["source_url"])
            values = (
                row["revision"],
                "M" + str(row["due_month"]),
                printed_date(row["due"]),
                printed_date(row["delivered"]),
                f"{row['variance_days']:+d}" if row["variance_days"] else "0",
            )
            for cell, value in zip(cells[1:], values):
                td(cell, value)
        if index == 0:
            p = doc.add_paragraph(
                "D3.5 và D3.6 cùng ghi 31/03/2025 và M30. Theo ngày trên bìa, cả hai trễ 122 ngày. Nếu dùng cuối M30 (30/06/2025), cả hai trễ 31 ngày. M1 bắt đầu tháng 01/2023. "
            )
            source_link(
                p,
                "Ngày bắt đầu dự án trên CORDIS",
                "https://cordis.europa.eu/project/id/101092639",
            )
        else:
            doc.add_paragraph(
                "D5.4 ghi hạn 31/03/2025 và M33 trên cùng bìa. Giao ngày 29/09/2025 tương ứng trễ 182 ngày theo hạn ghi ngày, hoặc sớm một ngày theo cuối M33. Cần lịch cơ sở đã duyệt để chốt đánh giá theo hợp đồng."
            )
            p = doc.add_paragraph(
                "D7.2 ghi ngày 28/11/2024 cho bản 1.1 nộp lại sau phản biện. Bản 1.0 ghi ngày 15/01/2024 ở trạng thái chuẩn bị nộp. Cần biên nhận để xác định ngày nộp lần đầu. "
            )
            source_link(
                p, "D7.2, lịch sử phiên bản, tr. 2", sources["D7.2"] + "#page=2"
            )
            p = doc.add_paragraph(
                "D6.1 ghi ngày giao 23/12/2023 trên bìa. D6.4 mô tả đã nộp D6.1 ở M10 và nộp lại ở M20. Sai lệch +53 ngày trong bảng chỉ đo bản có bìa đã dẫn. "
            )
            source_link(p, "D6.4, tr. PDF 88", sources["D6.4"] + "#page=88")
