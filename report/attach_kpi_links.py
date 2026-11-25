"""Attach native PDF-page links without discarding cached Excel summary formulas."""

import argparse
import json
from pathlib import Path
import sys
from zipfile import ZipFile

from lxml import etree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fame_pm.pilot_evaluation import page_url, read_evaluation

S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def linked_sheet(src, number, columns, records, *, freeze_identifiers=True):
    sheet_name = f"xl/worksheets/sheet{number}.xml"
    rel_name = f"xl/worksheets/_rels/sheet{number}.xml.rels"
    sheet = ET.fromstring(src.read(sheet_name))
    relationships = ET.fromstring(src.read(rel_name))
    links = ET.Element(S + "hyperlinks")
    sheet.find(S + "tableParts").addprevious(links)
    if freeze_identifiers:
        pane = sheet.find(".//" + S + "pane")
        pane.set("xSplit", "2")
        pane.set("topLeftCell", "C2")
        pane.set("activePane", "bottomRight")
        selection = sheet.find(".//" + S + "selection")
        if selection is not None:
            selection.set("pane", "bottomRight")
            selection.set("activeCell", "C2")
            selection.set("sqref", "C2")
    for i, urls in enumerate(records, 2):
        for col, url in zip(columns, urls):
            if url:
                ref = f"{col}{i}"
                rid = "link" + ref
                ET.SubElement(
                    links, S + "hyperlink", {"ref": ref, "{" + R + "}id": rid}
                )
                ET.SubElement(
                    relationships,
                    PKG + "Relationship",
                    Id=rid,
                    Type=R + "/hyperlink",
                    Target=url,
                    TargetMode="External",
                )
    return {
        sheet_name: ET.tostring(sheet, encoding="utf-8"),
        rel_name: ET.tostring(relationships, encoding="utf-8"),
    }


def attach(rows, authored, output):
    if authored.resolve() == output.resolve():
        raise ValueError("Use distinct input and output paths")
    keys = ("target_url", "actual_url", "period_url", "supporting_url")
    reviewed = sorted(
        (r["review"] for r in rows if r["review"]), key=lambda r: r["order"]
    )
    with ZipFile(authored) as src, ZipFile(output, "w") as dest:
        updated = linked_sheet(src, 2, "IJKL", ([r[k] for k in keys] for r in rows))
        updated.update(
            linked_sheet(
                src, 3, "IJ", ([s["url"] for s in r["sources"]] for r in reviewed)
            )
        )
        cases = sorted(
            (r for r in rows if r.get("execution")),
            key=lambda r: r["execution"]["order"],
        )
        updated.update(
            linked_sheet(
                src, 4, "KL", ((r["execution"]["url"], r["target_url"]) for r in cases)
            )
        )
        data, _ = read_evaluation()
        figures = [*data["pilots"], data["portfolio"]]
        updated.update(linked_sheet(src, 5, "G", ((page_url("d63", r["page"]),) for r in figures),
                                    freeze_identifiers=False))
        for info in src.infolist():
            dest.writestr(
                info,
                updated[info.filename] if info.filename in updated else src.read(info),
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("json_rows", "authored", "output"):
        parser.add_argument(key, type=Path)
    args = parser.parse_args()
    attach(
        json.loads(args.json_rows.read_text(encoding="utf-8")),
        args.authored,
        args.output,
    )
