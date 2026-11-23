"""Build the course submission using the published analysis and the editable UET layout."""

import argparse
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


def number(value, digits=0):
    value = Decimal(str(value)).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP)
    return f"{value:,.{digits}f}".translate(str.maketrans({",": ".", ".": ","}))


def report_fields(data):
    fields = {}
    fields["median_schedule"] = str(data["schedule"]["median_signed_days"])
    for row in data["schedule"]["deliverables"]:
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
    p.add_argument(
        "--pdf", action="store_true", help="Also export with LibreOffice and refresh index pages"
    )
    args = p.parse_args()
    subprocess.run([sys.executable, "-m", "fame_pm", "--check"], cwd=ROOT, check=True)
    binary = shutil.which("soffice") or os.getenv("SOFFICE")
    if args.pdf and not binary:
        p.error("--pdf requires soffice on PATH or SOFFICE pointing to its executable")
    args.out.mkdir(parents=True, exist_ok=True)
    data = json.loads((ROOT / "results/pm_results.json").read_text(encoding="utf-8"))
    doc = Document(ROOT / "report/mau_bien_tap.docx")
    fill(doc, report_fields(data))
    with tempfile.TemporaryDirectory(dir=args.out) as tmp:
        directory = Path(tmp)
        word = directory / (STEM + ".docx")
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
    print("Wrote report to", args.out.resolve())


if __name__ == "__main__":
    main()
