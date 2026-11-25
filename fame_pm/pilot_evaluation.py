"""Reconcile the seven published Innovation Pentagon figures and build the Pilot 5 case."""
import argparse
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path
import re

from .portfolio import BASE, ROOT, SOURCES, pages

GUIDE = ROOT / "docs/innovation-pentagon.md"
ZENODO = "https://zenodo.org/records/17175084"
DIMENSIONS = ["Market", "Customer", "Compliance", "Resources", "Technology"]


def page_url(doc, page):
    return f"{BASE}{SOURCES[doc][0]}#page={page}"


def read_evaluation():
    data = json.loads((ROOT / "evidence/innovation_pentagon.json").read_text(), parse_float=Decimal)
    pilots = data["pilots"]
    if data["dimensions"] != DIMENSIONS or [r["pilot"] for r in pilots] != list(range(1, 8)):
        raise ValueError("Unexpected pilot coverage or dimension order")
    for row in [*pilots, data["portfolio"]]:
        if len(row["scores"]) != len(DIMENSIONS) or not all(1 <= s <= 5 for s in row["scores"]):
            raise ValueError(f"Invalid scores in figure {row['figure']}")
    means = [(sum(column) / len(pilots)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
             for column in zip(*(r["scores"] for r in pilots))]
    if means != data["portfolio"]["scores"]:
        raise ValueError(f"Rounded column means {means} differ from FAME Figure 16")
    return data, means


def feedback():
    return json.loads((ROOT / "evidence/pilot5_feedback.json").read_text())


def weight_finding():
    weights = json.loads((ROOT / "results/open23_runs.json").read_text())["pilot5"]["weights"]
    trial = next(p for p in weights["profiles"] if p["weights_percent"] == [50, 25, 25])
    return (f"Trên ba tệp E/S/G gốc của Zenodo, người viết giữ nguyên {weights['tickers']} mã và từng dòng "
            f"đầu vào, thử {len(weights['profiles'])} cấu hình. So với ba trụ bằng nhau, tỷ trọng 50/25/25 "
            f"làm đổi thành phần top 5 ở {trial['rows_changing_top5_members_vs_equal']}/{weights['ordinal_rows']} dòng. "
            f"Bản xuất chỉ có {weights['unique_input_panels']} bộ điểm phân biệt và thiếu khóa ngày. "
            "Phép thử đo độ nhạy của cách xếp hạng do người viết lập trình.")


ACCEPTANCE = ("Người viết giữ mở P5-12 và P5-13. Để nghiệm thu, JRC/KM Cube cần cung cấp mã phiên bản và "
              "bản ghi kiểm thử ít nhất năm mức theo đặc tả trên đúng giao diện và bộ tối ưu. Mỗi ca ghi "
              "đầu vào, vector E/S/G hiển thị, cấu hình được nhận và khuyến nghị đầu ra. Để kiểm tra độc lập liên hệ "
              "giữa từng góp ý và bản phát hành, cần yêu cầu thay đổi, người phê duyệt và phiên bản bàn giao tương ứng.")


def vi(n):
    return f"{n:.2f}".replace(".", ",")


def verify_figures(directory, data):
    doc = pages(directory, "d63", False)
    for row in [*data["pilots"], data["portfolio"]]:
        name = f"Pilot {row['pilot']}" if "pilot" in row else "FAME"
        page = " ".join(doc[row["page"] - 1].split())
        caption = rf"Figure\s+{row['figure']}\s*:\s*{name}\s+overall evaluation"
        if not re.search(caption, page, flags=re.I):
            raise ValueError(f"Wrong source page for {name}")
    # Pilot numbers are printed inside the source images and were transcribed by eye.
    # Figure 16 also repeats the totals in prose, allowing a second, textual check.
    portfolio_text = " ".join(doc[data["portfolio"]["page"] - 1].split())
    for dimension, score in zip(DIMENSIONS, data["portfolio"]["scores"]):
        if not re.search(rf"\b{dimension}\s*\({re.escape(str(score))}\)", portfolio_text):
            raise ValueError(f"Published portfolio value differs for {dimension}")

    operations = pages(directory, "d62", False)
    requirements = pages(directory, "d64", False)
    anchors = [
        (doc, 54, "13 November 2025"), (doc, 55, "tool refinement"),
        (doc, 74, "refine weighting schemes"), (doc, 74, "improved reporting templates"),
        (operations, 45, "Figure 40"), (operations, 46, "Figure 41"),
        (requirements, 94, "P5_BR9"), (requirements, 70, "Independent E+S+G"),
    ]
    for document, number, phrase in anchors:
        if phrase.casefold() not in " ".join(document[number - 1].split()).casefold():
            raise ValueError(f"Missing Pilot 5 evidence on PDF page {number}: {phrase}")


def markdown(data, means):
    def source(doc, page):
        return f"[D{doc[1]}.{doc[2]} tr. {page}]({page_url(doc, page)})"

    lines = [
        "# Điểm Innovation Pentagon và quyết định quản lý ở Pilot 5", "",
        "## Bảy pilot được đánh giá như thế nào?", "",
        "Ở pha 1, các pilot và bên liên quan trả lời câu hỏi theo thang 1–5. FAME tổng hợp điểm theo năm chiều. "
        "Bộ Excel của FAME gồm bốn phần về kỹ thuật, kinh doanh, bảng hỏi Pentagon và hội thảo. Ở pha 2, "
        "FAME đối chiếu điểm trưởng thành với biến động KPI và ý kiến bên liên quan. Một điểm ở trục Compliance "
        "phản ánh tự đánh giá về tuân thủ. Để xác nhận một tỷ lệ tuân thủ cần dữ liệu kiểm toán riêng. "
        + " · ".join(source("d63", p) for p in (11, 12, 13, 76)), "",
        "Bảng chép nhãn số in ở năm ô bên dưới biểu đồ của từng pilot. Mỗi liên kết mở đúng trang PDF tính từ bìa. "
        "Hai dòng cuối phân biệt số FAME công bố với phép tính của người viết. Đơn vị là điểm trên thang 1–5.", "",
        "| Pilot | " + " | ".join(DIMENSIONS) + " | Nguồn |", "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in [*data["pilots"], data["portfolio"]]:
        title = f"Pilot {row['pilot']}" if "pilot" in row else "FAME công bố"
        link = f"[Hình {row['figure']}, tr. {row['page']}]({page_url('d63', row['page'])})"
        lines.append("| " + " | ".join([title, *map(vi, row["scores"]), link]) + " |")
    lines.extend(["| " + " | ".join(["Người viết tính lại", *map(vi, means), "Trung bình đều theo pilot"]) + " |", "",
        "Người viết lấy tổng bảy điểm đã in của mỗi chiều chia bảy, làm tròn một lần đến hai chữ số. "
        "Cả năm phép tính khớp Hình 16. Chưa có phiếu từng người, cỡ mẫu từng câu và quy tắc xử lý câu bỏ trống "
        "để tính lại điểm của mỗi pilot từ đầu hoặc ước lượng độ bất định.", "",
        "## Quyết định quản lý từ bảng điểm", "",
        "Phân tích của người viết. Điểm Technology bình quân là 3,28. Pilot 4 có Market 4,17 và Technology 2,33. "
        "Trước khi mở rộng, nên ưu tiên kiểm tra khả năng tích hợp và vận hành ở chính pilot này. "
        "Điểm Compliance 3,33 toàn dự án che khuất khoảng từ 1,00 ở Pilot 6 đến 5,00 ở Pilot 7. "
        "Người quản lý cần xem hồ sơ từng pilot trước khi phê duyệt rủi ro tuân thủ. "
        "Ở Pilot 5, Compliance đạt 4,60 nhưng KPI P5-08 yêu cầu ít nhất 80% danh mục đáp ứng tiêu chí ESG. "
        "Muốn đóng KPI phải có số danh mục đạt và tổng số danh mục được kiểm tra cùng kỳ. "
        + source("d63", 52) + " · [Ma trận nghiệm thu](../evidence/kpi_matrix.csv)", "",
        "## Pilot 5 từ phản hồi đến kiểm chứng", "",
        "D6.3 gọi M28–M36 (tháng 4–12/2025) là kỳ đánh giá pha 2 và vẫn liệt kê vòng nội bộ tháng 1 trong lịch tham gia. "
        "Giữ nguyên hai mốc của nguồn. Số người dự các buổi có thể trùng nhau. "
        + source("d63", 51) + " · " + source("d63", 54), ""])
    for row in feedback():
        links = " · ".join(source(d, p) for d, p in row["sources"])
        lines.extend([f"### {row['title']}", "", f"**{row['attribution']}.** {row['text']} {links}", ""])
    lines.extend(["### Tái kiểm của người viết và quyết định nghiệm thu", "", weight_finding()
                  + f" [Dữ liệu của tác giả]({ZENODO}) · [Đầu ra từng cấu hình](../results/open23_runs.json)", "",
                  ACCEPTANCE + " " + source("d64", 70)
                  + " · [Hồ sơ chứng cứ còn thiếu](../evidence/open23_requests.csv)", "",
                  "## Chạy lại từ thư mục gốc", "", "```bash",
                  "python -m pip install -r report/requirements.txt",
                  "python -m fame_pm.portfolio --data-dir du_lieu/portfolio --download --check",
                  "python -m fame_pm.pilot_evaluation --source-dir du_lieu/portfolio",
                  "```", "", "Lệnh cuối kiểm SHA-256 của ba PDF, tám chú thích hình, năm số tổng hợp và các đoạn bằng chứng Pilot 5. "
                  "Lệnh cũng đối chiếu bản Markdown với dữ liệu nguồn của bài. "
                  "Để rà lại 35 ô phiên chép, mở từng hình ở bảng trên. Dùng "
                  "`python -m fame_pm.pilot_evaluation --write` sau khi cập nhật nguồn. "
                  "[Dữ liệu bảng điểm](../evidence/innovation_pentagon.json) · "
                  "[Hướng dẫn chạy lại phép thử trọng số từ các CSV Zenodo](kiem-thu-23-kpi.md#cách-chạy-lại)"])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, help="Directory containing the three pinned FAME PDFs")
    parser.add_argument("--write", action="store_true", help="Regenerate the Markdown case study")
    args = parser.parse_args()
    evaluation, averages = read_evaluation()
    if args.source_dir:
        verify_figures(args.source_dir, evaluation)
    guide = markdown(evaluation, averages)
    if args.write:
        GUIDE.write_text(guide, encoding="utf-8")
    elif guide != GUIDE.read_text(encoding="utf-8"):
        raise SystemExit("Outdated case study. Regenerate it with --write.")
    print("Seven pilot figures reconciled with all five published portfolio scores.")
