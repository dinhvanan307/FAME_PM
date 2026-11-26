"""Run from the repository root: python -m fame_pm --check."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import BadZipFile

from .analysis import ROOT, pm_results, require
from .reviews import verify_reviews
from .sensitivity import panel_sensitivity


def esg_script(name, *args):
    script = ROOT / "esg-data-audit" / name
    output = subprocess.check_output([sys.executable, str(script), *map(str, args)], text=True)
    return json.loads(output)


def grouped_int(value):
    return f"{value:,}".replace(",", ".")


def summary_markdown(p):
    s, review = p["schedule"], p["independent_review"]
    lines = [
        "# Kết quả chạy lại phân tích FAME",
        "",
        "Sinh bằng `python -m fame_pm --write`. Tệp JSON cùng thư mục giữ số chưa làm tròn để trình bày.",
        "",
        "## Ngày bàn giao",
        "",
        "| Sản phẩm | Hạn gốc | Giao thực tế | Lệch ngày lịch |",
        "|---|---|---|---:|",
    ]
    for r in s["deliverables"]:
        lines.append(
            f"| [{r['deliverable']}]({r['source_url']}) | {r['due']} | {r['delivered']} | {r['variance_days']:+} |"
        )
    lines += [
        "",
        f"Hạn đến bản phản biện D6.4: {s['d64_before_review_days']} ngày. Từ đó đến bàn giao: "
        f"{s['d64_after_review_days']} ngày. Trung vị sai lệch có dấu của năm sản phẩm: {s['median_signed_days']} ngày.",
        "",
        "## Nghiệm thu Pilot 5",
        "",
        "| KPI | Chỉ tiêu | Tham chiếu tài liệu | Quyết định theo quy tắc |",
        "|---|---|---|---|",
    ]
    for k in p["kpis"]:
        lines.append(
            f"| {k['id']} | {k['label']} | [Ngưỡng]({k['target_source']}) · "
            f"[Kết quả dự án]({k['observation_source']}) | {k['decision']} |"
        )
    lines += ["", "## Hai phép so sánh quản lý", "", "| Chỉ số | A | B |", "|---|---:|---:|"]
    for title, metric in [
        ("Hồ sơ mở có đầu mối đề xuất (hồi cứu)", "with_owner"),
        ("Quyết định khớp tham chiếu (hồi cứu)", "matches"),
    ]:
        lines.append(
            f"| {title} | {p['retrospective']['A'][metric]} | {p['retrospective']['B'][metric]} |"
        )
    for title, metric in [
        ("Khớp tham chiếu độc lập / 6", "matches"),
        ("Duyệt khi thiếu chứng cứ / 3", "false_approvals"),
        ("Trung bình giây/KPI", "mean_seconds"),
        ("Trung vị giây/KPI", "median_seconds"),
    ]:
        lines.append(f"| {title} | {review['A'][metric]} | {review['B'][metric]} |")
    lines += [
        "",
        "## Cơ cấu tài trợ",
        "",
        "| Phạm vi | Tổng EUR | EU EUR | Phần còn lại EUR | EU (%) |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in p["funding"]:
        lines.append(
            "| {name} | {cost_eur} | {eu_eur} | {other_eur} | {eu_share_pct} |".format(**row)
        )
    e = p["esg"]
    confirmation = e["confirmation"]
    panel = e["all_rows_sensitivity"]
    lines += [
        "",
        "## Phép tái lập dữ liệu ESG",
        "",
        f"**Lần đầu (21/11/2026).** Ghép duy nhất với một chuỗi ngành cho {e['tickers']} mã. "
        f"Trên {e['test_rows']} dòng đối chiếu, {grouped_int(e['matched'])}/{grouped_int(e['cells'])} ô E/S/G của tập này khớp. "
        f"Đối chứng giữ điểm gốc khớp {e['unchanged_matches']} ô. "
        "[Phép đo ban đầu](../esg-data-audit/reproduction.json)",
        "",
        f"**Lượt xác nhận (25/11/2026).** Dùng trung bình tám ngành theo từng dòng cho "
        f"{len(e['unmatched'])} mã ngoại lệ. Trên cùng bản Zenodo v1, phạm vi đã kiểm tăng "
        f"từ {e['tickers']} lên đủ {confirmation['tickers']} mã. "
        f"Cả {grouped_int(confirmation['matched'])}/{grouped_int(confirmation['denominator'])} ô E/S/G khớp. "
        "Bảng phân ngành nội bộ vẫn cần tác giả xác nhận. "
        "[Phép đo xác nhận](../Pilot5_nghiem_thu/phep_do.json)",
        "",
        f"Hai hồ sơ trọng số giữ cùng thành phần top 5 ở {panel['identical_members']}/{panel['rows']} dòng. "
        f"Có {panel['different_members']} dòng thay thành phần và {panel['identical_order']} dòng giữ nguyên thứ tự. "
        f"Có {panel['distinct_top5_pairs']} cặp danh sách có thứ tự khác nhau trong toàn bộ bản xuất. "
        f"Số dòng có đồng điểm ở ranh hạng 5 và 6 trong ít nhất một hồ sơ: {panel['cutoff_tie_rows']}.",
        "",
        "Có thể tải lại dữ liệu gốc bằng tùy chọn `--download --data-dir`. "
        "Chế độ mặc định dùng bản kết quả ESG đã lưu trong Git.",
        "",
        "[Phân tích các miền tri thức](../docs/phan-tich-quan-ly.md) · "
        "[Hồ sơ và giới hạn nguồn](../evidence/README.md)",
        "",
    ]
    return "\n".join(lines)


def encoded(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def atomic_text(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=path.parent, mode="w", encoding="utf-8", delete=False
    ) as temp:
        temp.write(value)
    try:
        os.replace(temp.name, path)
    finally:
        Path(temp.name).unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="Regenerate the tracked PM outputs")
    mode.add_argument("--check", action="store_true", help="Verify tracked outputs (default)")
    parser.add_argument(
        "--data-dir", type=Path, help="Verify all original Zenodo CSVs in this directory"
    )
    parser.add_argument(
        "--download", action="store_true", help="Download the pinned Zenodo record before verifying"
    )
    parser.add_argument(
        "--reviews-dir",
        type=Path,
        help="Privately verify the two original review CSVs against published totals",
    )
    args = parser.parse_args()
    if args.download and not args.data_dir:
        parser.error("--download requires --data-dir")
    p = pm_results()
    published = json.loads((ROOT / "esg-data-audit/reproduction.json").read_text(encoding="utf-8"))
    audit_path = ROOT / "evidence/esg_audit.json"
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    panel_path = ROOT / "results/ranking_sensitivity.json"
    if args.data_dir:
        options = ["--data-dir", args.data_dir]
        rerun = esg_script(
            "reproduce_pilot5.py", *options, *(["--download"] if args.download else [])
        )
        require(rerun == published, "ESG reproduction differs from the published JSON")
        require(
            esg_script("audit.py", *options) == audit, "CSV audit differs from the published JSON"
        )
        panel = panel_sensitivity(args.data_dir, rerun)
    else:
        panel = json.loads(panel_path.read_text(encoding="utf-8"))
    pillars = published["held_out"].values()
    confirmed = json.loads((ROOT / "Pilot5_nghiem_thu/phep_do.json").read_text(encoding="utf-8"))
    require(confirmed["doi"] == published["doi"] and
            confirmed["baseline_matched"] == sum(v["matched"] for v in pillars) and
            [r["ticker"] for r in confirmed["exceptions"]] == published["unmatched_tickers"],
            "Pilot 5 confirmation does not match the original run")
    p["esg"] = dict(
        doi=published["doi"],
        tickers=published["unique_series_matched"],
        test_rows=published["test_rows"][1] - published["test_rows"][0] + 1,
        matched=sum(v["matched"] for v in pillars),
        cells=sum(v["cells"] for v in pillars),
        unchanged_matches=sum(v["unchanged_matches"] for v in pillars),
        unmatched=published["unmatched_tickers"],
        confirmation={key: confirmed[key] for key in ("tickers", "matched", "denominator")},
        quality=audit,
        ranking_sensitivity=published["ranking_sensitivity"],
        all_rows_sensitivity=panel,
    )
    if args.reviews_dir:
        verify_reviews(args.reviews_dir, p)
    outputs = {
        "pm_results.json": encoded(p),
        "ket-qua.md": summary_markdown(p),
        "ranking_sensitivity.json": encoded(panel),
    }
    for name, content in outputs.items():
        path = ROOT / "results" / name
        if args.write:
            atomic_text(path, content)
        else:
            require(
                path.is_file() and path.read_text(encoding="utf-8") == content,
                f"Stale/missing {path.name}",
            )
    print(
        "PM outputs:",
        "written" if args.write else "verified",
        "| ESG:",
        "original CSVs verified" if args.data_dir else "published snapshot",
        "| independent reviews:",
        "source CSVs verified" if args.reviews_dir else "published aggregates",
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, BadZipFile, subprocess.CalledProcessError) as exc:
        sys.exit(f"FAME analysis failed: {exc}")
