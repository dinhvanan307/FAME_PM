"""Build the course submission using the published analysis and the editable UET layout."""

import argparse
import csv
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from docx import Document
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
STEM = "FAME_Bao_cao_cuoi_ky"
sys.path.insert(0, str(ROOT))
# ruff: noqa: E402 -- direct script execution needs the repository imports below.
from Pilot5_nghiem_thu.tong_hop import PUBLIC_RESULT, report_review
from fame_pm.qa_capacity import make_jobs, metrics
from fame_pm.review_scenario import scenarios
from report.appendix_directory import add_appendix_directory
from report.kpi_appendix import append_register
from report.pilot_evaluation import add_pilot_evaluation
from report.pilot5_acceptance import append_acceptance
from report.marketsense_sp100 import append_marketsense
from report.schedule import append_schedule
from report.risk_chapter import fill_risk_chapter


def number(value, digits=0):
    value = Decimal(str(value)).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP)
    return f"{value:,.{digits}f}".translate(str.maketrans({",": ".", ".": ","}))


def report_fields(data):
    fields = {}
    schedule = data["schedule"]
    fields["median_schedule"] = number(schedule["median_signed_days"])
    fields["schedule_total"] = str(len(schedule["deliverables"]))
    for key in ("late", "early", "on_deadline"):
        fields["schedule_" + key] = str(schedule[key])
    for wp, counts in schedule["by_work_package"].items():
        prefix = wp.lower() + "_"
        for key, source in (("total", "reports"), ("early", "early"), ("exact", "on_deadline"), ("late", "late")):
            fields[prefix + key] = str(counts[source])
    sensitivity = schedule["excluding_annotated_covers"]
    fields["sensitivity_total"] = str(sensitivity["reports"])
    fields["sensitivity_late"] = str(sensitivity["late"])
    fields["sensitivity_median"] = number(sensitivity["median_signed_days"])
    fields["d64_before"] = str(schedule["d64_before_review_days"])
    fields["d64_delta"] = str(schedule["d64_before_review_days"] + schedule["d64_after_review_days"])

    branches = scenarios()
    for branch in branches:
        prefix = branch["case"].lower() + "_"
        fields[prefix + "wait"] = str(branch["wait_days"])
        fields[prefix + "slip"] = str(branch["versus_cover_days"])
        for key in ("feedback", "finish"):
            fields[prefix + key] = date.fromisoformat(branch[key]).strftime("%d/%m/%Y")
    fields["recovered_days"] = str(branches[1]["wait_days"] - branches[2]["wait_days"])
    jobs = make_jobs()
    qa = metrics(jobs)
    for job in jobs:
        key = job.plan + "_" + job.code.replace(".", "_")
        fields["qa_" + key] = job.finish.strftime("%d/%m/%Y")
    for plan, values in qa.items():
        for key in ("request_excess", "feasible_excess", "on_target"):
            fields[f"qa_{plan}_{key}"] = str(values[key])
    fields["qa_earlier"] = str((qa["A"]["last"] - qa["B"]["last"]).days)
    review = data["independent_review"]
    for key, stat in (("mean", "delta_mean_seconds"), ("median", "delta_median_seconds")):
        delta = review[stat]
        fields[f"click_{key}_delta"] = ("+" if delta > 0 else "−" if delta < 0 else "") + number(abs(delta), 3)
    fields["review_gain_pp"] = number(review["B"]["accuracy_pct"] - review["A"]["accuracy_pct"])
    retro = data["retrospective"]
    fields["owner_gain_pp"] = number(100 * (retro["B"]["with_owner"] / retro["B"]["open"]
                                            - retro["A"]["with_owner"] / retro["A"]["open"]))

    confirmed = json.loads((ROOT / "Pilot5_nghiem_thu/phep_do.json").read_text(encoding="utf-8"))
    fields["confirmed_tickers"] = str(confirmed["tickers"])
    for field, source in (("confirmed_matches", "matched"), ("confirmed_cells", "denominator")):
        fields[field] = number(confirmed[source])
        fields[field + "_en"] = format(confirmed[source], ",d")
    for row in schedule["deliverables"]:
        k = row["deliverable"].replace(".", "_")
        fields[k + "_due"] = date.fromisoformat(row["due"]).strftime("%d/%m/%Y")
        fields[k + "_actual"] = date.fromisoformat(row["delivered"]).strftime("%d/%m/%Y")
        fields[k + "_late"] = f"{row['variance_days']:+d} ngày".replace("-", "−")
    for i, row in enumerate(data["funding"]):
        for k in ["cost_eur", "eu_eur", "other_eur", "eu_share_pct"]:
            fields[f"f{i}_{k}"] = number(row[k], 2) + ("%" if k.endswith("pct") else "")
    fields["other_pct"] = number(100 - Decimal(str(data["funding"][0]["eu_share_pct"])), 2) + "%"
    for mode in ("A", "B"):
        h = data["retrospective"][mode]
        a = data["independent_review"][mode]
        fields["retro_match_" + mode] = f"{h['matches']}/{len(data['kpis'])}"
        fields["retro_owner_" + mode] = f"{h['with_owner']}/{h['open']}"
        fields["review_match_" + mode] = f"{a['matches']}/{a['n']} ({number(a['accuracy_pct'])}%)"
        fields["review_false_" + mode] = f"{a['false_approvals']}/{a['missing_evidence_cases']}"
        fields["review_mean_" + mode] = number(a["mean_seconds"], 3)
        fields["review_median_" + mode] = number(a["median_seconds"], 3)
    e = data["esg"]
    for key in ("matched", "cells", "tickers", "test_rows"):
        fields["esg_" + key] = number(e[key])
    for key, v in e["all_rows_sensitivity"].items():
        if type(v) is int:
            fields["rank_" + key] = number(v)
    fields["overlap_three"] = str(e["all_rows_sensitivity"]["overlap_histogram"]["3"])
    fields["open_ids"] = ", ".join(
        row["id"] for row in data["kpis"] if row["decision"] == "Thiếu bằng chứng"
    )
    return fields


def fill(doc, fields):
    # Tokens occupy a single text run in the authoring template. Preserve styles and links.
    used = set()
    for text in doc.element.body.xpath(".//w:t"):

        def substitute(match):
            key = match.group(1)
            used.add(key)
            return fields[key]

        text.text = re.sub(r"\[\[([a-zA-Z0-9_]+)\]\]", substitute, text.text or "")
    if not used or "[[" in "".join(doc.element.body.itertext()):
        raise ValueError("Missing or fragmented report fields")


def append_portfolio(doc):
    portfolio = json.loads((ROOT / "results/pilot_portfolio.json").read_text(encoding="utf-8"))
    upstream = json.loads((ROOT / "results/pilot7_boundaries.json").read_text(encoding="utf-8"))
    with (ROOT / "evidence/pilot-outcomes.csv").open(encoding="utf-8", newline="") as source:
        findings = {int(row["pilot"]): row for row in csv.DictReader(source)}
    if list(findings) != [p["pilot"] for p in portfolio["pilots"]]:
        raise ValueError("Pilot findings do not match the PDF index")

    def title(text):
        paragraph = doc.add_paragraph(text, style="Heading 2")
        paragraph.paragraph_format.page_break_before = True

    title("F  Kết quả của bảy thí điểm FAME")
    doc.add_paragraph(
        f"Bảng 1 của D6.4 liệt kê {len(findings)} pilot với {portfolio['total_use_cases']} ca sử dụng. "
        "D6.2 mô tả vận hành từng pilot. D6.3 ghi kết quả đánh giá. Các dẫn trang dưới đây "
        "dùng số trang của tệp PDF, tính cả trang bìa. Số liệu trong câu đầu mỗi mục do "
        "FAME báo cáo. Phần tiếp theo nêu nhận định quản lý của người viết."
    )
    for pilot in portfolio["pilots"]:
        n = pilot["pilot"]
        row = findings[n]
        if n == 5:
            title("F  Kết quả thí điểm tài chính và dữ liệu công nghiệp")
        paragraph = doc.add_paragraph()
        paragraph.add_run(f"Pilot {n} · {row['name_vi']}. ").bold = True
        paragraph.add_run(row["consortium_observation"])
        page = row["evaluation_pdf_page"]
        # Table 5 contains the three reported Pilot 5 figures on separate pages.
        locator = f"{page}–54" if n == 5 else page
        paragraph.add_run(f" [D6.3, Bảng {n}, tr. PDF {locator}]")
        doc.add_paragraph(row["author_assessment"])
    tested = upstream["tested_tags"]
    checks = upstream["passed_boundary_cases"]
    doc.add_paragraph(
        f"Thực nghiệm Pilot 7. Hàm kiểm tra ngưỡng từ kho mã IIoT của đối tác cho "
        f"kết quả dự kiến ở {checks}/{checks} ca biên trên {tested}/{upstream['configured_rows']} "
        "cảm biến cấu hình. Giá trị đầu vào do người viết tạo từ ngưỡng của tác giả. "
        "Hai cảm biến thiếu loại ngưỡng. Ở mã 75PI823, giá trị CSV có dấu phẩy khác với "
        "SQL khởi tạo. Đề xuất giữ mở ngoại lệ tới khi bên vận hành xác nhận đơn vị và cách nạp. "
        "[D6.4, Bảng 53, tr. PDF 80–81]"
    )
    from docx.opc.constants import RELATIONSHIP_TYPE
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    paragraph = doc.add_paragraph("Nguồn và cách chạy. ", style="Minicap")
    for label, url in [
        ("D6.2", portfolio["sources"]["d62"]["url"]),
        ("D6.3", portfolio["sources"]["d63"]["url"]),
        ("D6.4", portfolio["sources"]["d64"]["url"]),
        ("Mã Pilot 7", upstream["upstream"] + "/tree/" + upstream["commit"]),
        ("Bản rà và lệnh tái lập", "https://github.com/dinhvanan307/FAME_PM/blob/main/docs/ra-soat-truoc-khi-nop.md"),
    ]:
        link = OxmlElement("w:hyperlink")
        link.set(qn("r:id"), paragraph.part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True))
        run = paragraph.add_run(label)
        run.font.underline = True
        link.append(run._r)
        paragraph._p.append(link)
        if label != "Bản rà và lệnh tái lập":
            paragraph.add_run(" · ")


def export_pdf(binary, docx, directory):
    with tempfile.TemporaryDirectory() as profile:
        cmd = [
            binary,
            "-env:UserInstallation=" + Path(profile).resolve().as_uri(),
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(directory),
            str(docx),
        ]
        subprocess.run(cmd, check=True, capture_output=True)
    pdf = directory / (STEM + ".pdf")
    if not pdf.is_file() or pdf.stat().st_size == 0:
        raise RuntimeError("LibreOffice did not produce the PDF")
    return pdf


def update_index_cache(doc, pdf):
    # Word stores cached page numbers separately from the clickable destinations.
    # Derive printed numbers from the actual render, including unnumbered covers.
    reader = PdfReader(pdf)
    printed = {}
    for page in reader.pages:
        lines = page.extract_text().strip().splitlines()
        if lines and lines[0].strip().isdigit():
            printed[page.indirect_reference.idnum] = int(lines[0].strip())
    fields = [p for p in doc.paragraphs if p._p.xpath("./w:hyperlink[@w:anchor]")]
    resolved = []
    for page in reader.pages:
        indices = [
            int(m[1])
            for line in page.extract_text().splitlines()
            if (m := re.search(r"\.{2,}\s*(\d+)\s*$", line))
        ]
        if not indices:
            continue
        positions = set()
        for ref in page.get("/Annots", []):
            a = ref.get_object()
            dest = a.get("/Dest")
            if isinstance(dest, list) and hasattr(dest[0], "idnum") and dest[0].idnum in printed:
                positions.add((round(float(a["/Rect"][1]), 1), printed[dest[0].idnum]))
        actual = [n for _, n in sorted(positions, reverse=True)]
        if len(actual) != len(indices):
            raise ValueError("Could not match all rendered index entries")
        resolved.extend(actual)
    if len(fields) != len(resolved):
        raise ValueError("Incomplete PDF index")
    changed = False
    for field, n in zip(fields, resolved):
        el = field._p.xpath("./w:r/w:t")[-1]
        changed |= el.text != str(n)
        el.text = str(n)
    return changed


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, default=ROOT, help="Output directory")
    p.add_argument("--pilot5-ballots", type=Path,
                   help="Directory containing returned P1.xlsx and/or P2.xlsx (default: du_lieu/phieu_pilot5)")
    p.add_argument(
        "--pdf", action="store_true", help="Also export with LibreOffice and refresh index pages"
    )
    args = p.parse_args()
    try:
        review = report_review(args.pilot5_ballots)
    except (KeyError, ValueError) as exc:
        p.error(str(exc))
    subprocess.run([sys.executable, "-m", "fame_pm", "--check"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "-m", "fame_pm.review_scenario", "--check"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "-m", "fame_pm.qa_capacity", "--check"], cwd=ROOT, check=True)
    binary = shutil.which("soffice") or os.getenv("SOFFICE")
    if args.pdf and not binary:
        p.error("--pdf requires soffice on PATH or SOFFICE pointing to its executable")
    args.out.mkdir(parents=True, exist_ok=True)
    data = json.loads((ROOT / "results/pm_results.json").read_text(encoding="utf-8"))
    doc = Document(ROOT / "report/mau_bien_tap.docx")
    fill_risk_chapter(doc, data["kpis"])
    fill(doc, report_fields(data))
    append_portfolio(doc)
    append_register(doc)
    add_pilot_evaluation(doc)
    append_acceptance(doc, review)
    append_marketsense(doc)
    append_schedule(doc, data["schedule"])
    add_appendix_directory(doc)
    if not args.pdf:
        # A Word-only export can reuse the released field cache without a renderer.
        # New anchors are resolved by Word or by a subsequent --pdf build.
        released = ROOT / (STEM + ".docx")
        if released.is_file():
            cached = {}
            for para in Document(released).paragraphs:
                anchor = para._p.xpath("./w:hyperlink/@w:anchor")
                if anchor:
                    cached[anchor[0]] = para._p.xpath("./w:r/w:t")[-1].text
            for para in doc.paragraphs:
                anchor = para._p.xpath("./w:hyperlink/@w:anchor")
                if anchor and anchor[0] in cached:
                    para._p.xpath("./w:r/w:t")[-1].text = cached[anchor[0]]
    with tempfile.TemporaryDirectory(dir=args.out) as tmp:
        directory = Path(tmp)
        word = directory / (STEM + ".docx")
        snapshot = directory / PUBLIC_RESULT.name
        snapshot.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        published = args.out / PUBLIC_RESULT
        published.parent.mkdir(parents=True, exist_ok=True)
        doc.save(word)
        if args.pdf:
            pdf = export_pdf(binary, word, directory)
            if update_index_cache(doc, pdf):
                doc.save(word)
                pdf.unlink()
                pdf = export_pdf(binary, word, directory)
                if update_index_cache(doc, pdf):
                    raise ValueError("Index pagination did not stabilize")
            os.replace(pdf, args.out / pdf.name)
        os.replace(word, args.out / word.name)
        os.replace(snapshot, published)
    print("Wrote report to", args.out.resolve())


if __name__ == "__main__":
    main()
