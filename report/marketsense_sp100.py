"""Render the Pilot 5 evidence pages from the published signal audit."""
import csv
import json
from pathlib import Path

from report.kpi_appendix import heading, source_link, table, td

ROOT = Path(__file__).resolve().parents[1]
AUDIT = "https://github.com/dinhvanan307/FAME_PM/tree/main/esg-data-audit/marketsense-sp100"
SNAPSHOT = ("https://www.fame-horizon.eu/wp-content/uploads/2026/02/"
            "FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf#page=64")


def integer(n):
    return f"{n:,}".replace(",", ".")


def append_marketsense(doc):
    data = json.loads((ROOT / "results/marketsense_sp100.json").read_text(encoding="utf-8"))
    with (ROOT / "results/marketsense_sp100.csv").open(encoding="utf-8", newline="") as source:
        joined = [row for row in csv.DictReader(source) if row["d64_key_matched"] == "1"]
    n = data["observations"]
    labels = (("buy", "Mua"), ("hold", "Giữ"), ("sell", "Bán"))
    heading(doc, "K  Tín hiệu MarketSenseAI và lời giải thích")
    doc.add_paragraph(
        f"Trên {integer(n)} quyết định, tín hiệu giữ chiếm tỷ lệ cao nhất. Người viết đếm lại từ "
        f"CSV gốc của Fatouros và Metaxas, gồm {data['unique_tickers']} mã S&P 100 ở "
        f"{len(data['by_date'])} ngày cuối tháng. Tệp có cả ngày 31/12/2022, trước mốc "
        "01/01/2023 trong mô tả Zenodo. Kỳ cuối là 29/02/2024."
    )
    t = table(doc, ["Tín hiệu", "Số quan sát", "Tỷ lệ", "Trung vị số từ trong lý do"], [3.2, 3.5, 3.0, 5.7])
    for label, name in labels:
        count = data["by_decision"][label]
        values = (name, integer(count), f"{count / n:.2%}".replace(".", ","),
                  str(int(data["median_words_by_decision"][label])))
        for cell, value in zip(t.add_row().cells, values):
            td(cell, value)
    january = data["by_date"]["2024-01-31"]
    february = data["by_date"]["2024-02-29"]
    doc.add_paragraph(
        f"Tháng 01/2024 có {january['buy']} tín hiệu mua, {january['hold']} giữ và "
        f"{january['sell']} bán. Tháng kế tiếp có {february['buy']} mua, {february['hold']} giữ "
        f"và {february['sell']} bán. Chỉ {data['by_decision']['sell']} tín hiệu bán xuất hiện "
        "trong toàn bộ 15 kỳ, nên một quyết định đơn lẻ đã làm thay đổi đáng kể tỷ lệ của nhóm này."
    )
    markers = data["marker_counts_by_decision"]
    fundamentals = sum(markers[k]["fundamentals"] for k, _ in labels)
    esg = sum(markers[k]["explicit_esg"] for k, _ in labels)
    doc.add_paragraph(
        f"Cả {integer(data['explanations_present'])} quan sát có lời giải thích. Quy tắc từ khóa tìm "
        f"thấy từ ngữ về nền tảng doanh nghiệp ở {integer(fundamentals)} dòng và tên ESG hoặc cụm "
        f"đầy đủ tiếng Anh ở {esg} dòng. Mỗi chủ đề được đếm tối đa một lần trên một dòng. "
        "Số đếm mô tả cách diễn đạt. Muốn xác minh nội dung phải đối chiếu tiếp với nguồn tin "
        "và báo cáo tài chính tại thời điểm phát tín hiệu."
    )
    doc.add_paragraph(
        "Ba ví dụ đọc từ trường why. Với Apple ngày 31/08/2023 (ID 1), mô hình cân nhắc tăng "
        "trưởng dịch vụ với doanh thu và khả năng sinh lời suy giảm, rồi chọn giữ. Đến 31/12/2023 "
        "(ID 0), mô hình nhấn mạnh vị thế thị trường, lợi nhuận và dòng tiền để giải thích quyết "
        "định mua. Với Boeing ngày 31/01/2024 (ID 191), mô hình viện dẫn sự cố vận hành, biến "
        "động giá và dòng tiền yếu để giải thích quyết định bán."
    )
    p = doc.add_paragraph(style="Minicap")
    source_link(p, "CSV tác giả · Zenodo v1", "https://zenodo.org/records/12744005")
    p.add_run("   ·   ")
    source_link(p, "Nghiên cứu MarketSenseAI", "https://doi.org/10.1007/s00521-024-10613-4")
    p.add_run("   ·   ")
    source_link(p, "Thống kê theo tháng, từ khóa và mã tái lập", AUDIT)

    heading(doc, "K  Ghép tín hiệu với điểm ESG theo mã và ngày")
    snapshot = data["d64_pdf_page_64"]
    original = data["zenodo_esg"]
    doc.add_paragraph(
        f"Bộ CSV ESG của Pilot 5 có {original['shared_tickers']} mã trùng với MarketSenseAI. "
        f"Mỗi bảng E, S, G có {original['raw_pillar_rows']['e']} dòng, với các mã cổ phiếu "
        "làm tiêu đề cột. Do thiếu ngày của từng dòng, số cặp mã và ngày xác minh trực tiếp "
        "từ bộ CSV ESG là 0. Khoảng thời gian ghi trong tên tệp chỉ mô tả phạm vi bản xuất."
    )
    doc.add_paragraph(
        "Ảnh bảng xếp hạng ở trang PDF 64 của D6.4 có khóa thời gian sử dụng được. Bảng đề "
        "tháng 3/2024, còn trường Predicted at ghi 29/02/2024. Người viết chép các dòng nhìn "
        f"thấy và ghép theo đúng mã cùng ngày dự báo. Ghép được {len(joined)}/{snapshot['visible_rows']} "
        f"dòng ảnh, tương ứng {len(joined)} trong {sum(february.values())} mã của kỳ đó. "
        f"Cả {snapshot['same_signal']} dòng đều ghi mua ở hai nguồn. Ví dụ dưới đây giữ "
        "thang điểm hiển thị của FAME. Ảnh chỉ ghi ngày dự báo của bảng, không ghi ngày "
        "đo riêng cho từng điểm E, S, G."
    )
    t = table(doc, ["Mã", "Tín hiệu hai nguồn", "E", "S", "G"], [3.3, 4.3, 2.6, 2.6, 2.6])
    for row in [r for r in joined if r["ticker"] in {"JPM.US", "MSFT.US", "SPG.US"}]:
        values = [row["ticker"], "Mua / Mua"] + [row[f"d64_{p}"].replace(".", ",") for p in ("env", "soc", "gov")]
        for cell, value in zip(t.add_row().cells, values):
            td(cell, value)
    day = snapshot["source_dates"][0]
    doc.add_paragraph(
        f"Nhận định của người viết. Ảnh chỉ bao phủ {len(joined)} trong "
        f"{data['by_date'][day]['buy']} mã có tín hiệu mua ngày đó. "
        f"Còn {integer(snapshot['signal_rows_without_snapshot'])} quan sát thiếu điểm ESG ghép được. "
        f"PM chấp nhận {len(joined)} dòng truy vết đến ảnh. Ngày cập nhật từng điểm ESG và các kỳ còn lại "
        "cần thêm bằng chứng. Tập con chỉ có nhãn mua nên chưa thể đánh giá tác động của ESG "
        "lên lựa chọn mua, giữ hoặc bán. R4 và R6 vẫn cần năm cấu hình trọng số từ công cụ gốc."
    )
    p = doc.add_paragraph(style="Minicap")
    source_link(p, "D6.4 · ảnh gốc trang PDF 64", SNAPSHOT)
    p.add_run("   ·   ")
    source_link(p, "Bộ ESG v1", "https://zenodo.org/records/17175084")
    p.add_run("   ·   ")
    source_link(p, "Bảng ghép và bản chép từng dòng", AUDIT)

    review = data["source_review"]
    heading(doc, "K  Rà nguồn bổ sung cho các tín hiệu còn thiếu ESG")
    end_date = data["date_range"][-1]
    with (ROOT / "evidence/pilot5_esg_pdf_screen.csv").open(encoding="utf-8", newline="") as stream:
        reports = list(csv.DictReader(stream))
    doc.add_paragraph(
        f"Ngày 27/11/2026, người viết sàng lọc lớp văn bản của {len(reports)} báo cáo FAME "
        f"({integer(sum(int(r['pdf_pages']) for r in reports))} trang PDF), xem hình ở các trang liên quan, "
        "đối chiếu bản giới thiệu Pilot 5, ba bộ slide webinar, ảnh Showcase và năm video. "
        f"Trước khi rà có {review['baseline']} khóa đã xác minh. Số khóa mới đủ điều kiện là "
        f"{review['added']}. Tổng sau khi rà là {review['verified']}/{integer(n)}."
    )
    t = table(doc, ["Nguồn gốc", "Điều đọc được từ FAME", "Kết luận của người viết"], [3.3, 6.6, 5.5])
    items = [
        ("KM Cube, slide 14", "Ví dụ NVIDIA có E/S/G riêng cho các năm 2016, 2017 và 2018.",
         "Chỉ có năm và cả ba năm đều trước 31/12/2022."),
        ("D6.2, hình 41, tr. 46", "ABBV.US xuất hiện trong bảng. Ngày lọc 21/09/2025, ngày dữ liệu 19/09/2025.",
         "Ngoài kỳ. ESG Rank là điểm xếp hạng tổng hợp."),
        ("Webinar 4, 30:18 và 31:52", "Màn hình xếp hạng tháng 9/2025, tiếp theo là cơ cấu danh mục tối ưu.",
         "Các cột xếp hạng và tỷ trọng không cung cấp bộ điểm E/S/G theo mã."),
        ("D1.4, bảng 27, tr. 47", "Mô tả một bản xếp hạng JSON được tái tạo hằng tháng.",
         "Cần lấy bản xuất có mã, ngày và ba điểm để kiểm chứng từng dòng."),
    ]
    for item in items:
        for cell, value in zip(t.add_row().cells, item):
            td(cell, value)
    verified = review["verified"]
    remaining = review["open"]
    final_month = sum(data["by_date"][end_date].values()) - len(joined)
    doc.add_paragraph(
        f"Quyết định nghiệm thu của người viết. Bảng D6.4 vẫn cung cấp {verified} khóa có "
        f"nguồn cấp dòng. Trong {integer(remaining)} khóa còn mở, {final_month} thuộc "
        "ngày 29/02/2024, phần còn lại thuộc 14 kỳ trước. Muốn bổ sung cần bảng thành phần "
        "theo mã, ngày dự báo hoặc ngày hiệu lực, kèm định nghĩa thang điểm. "
        "Các video bổ trợ được lấy mẫu theo thời gian nên có thể bỏ sót khung hình ngắn."
    )
    p = doc.add_paragraph(style="Minicap")
    for i, (label, url) in enumerate([
        ("Slide 14", "https://zenodo.org/records/17937391/files/fame_presentation%20%282%29.pdf#page=14"),
        ("D6.2, tr. 46", next(r["url"] for r in reports if r["report"] == "D6.2") + "#page=46"),
        ("Video 30:18", "https://www.youtube.com/watch?v=cmfj7OEz2Ow&t=1818s"),
        ("Video 31:52", "https://www.youtube.com/watch?v=cmfj7OEz2Ow&t=1912s"),
        ("D1.4, tr. 47", next(r["url"] for r in reports if r["report"] == "D1.4") + "#page=47"),
        ("Sổ rà nguồn", "https://github.com/dinhvanan307/FAME_PM/blob/main/esg-data-audit/marketsense-sp100/ra-soat-nguon.md"),
        ("CSV từng mã, ngày và nguồn", "https://github.com/dinhvanan307/FAME_PM/blob/main/results/marketsense_esg_matches.csv"),
    ]):
        if i:
            p.add_run("   ·   ")
        source_link(p, label, url)
