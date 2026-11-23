"""Attach native PDF-page links without discarding cached Excel summary formulas."""

import argparse
import json
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as ET

SHEET = "xl/worksheets/sheet2.xml"
RELS = "xl/worksheets/_rels/sheet2.xml.rels"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def attach(rows, authored, output):
    if authored.resolve() == output.resolve():
        raise ValueError("Use distinct input and output paths")
    with ZipFile(authored) as src, ZipFile(output, "w") as dest:
        sheet = ET.fromstring(src.read(SHEET))
        relationships = ET.fromstring(src.read(RELS))
        links = ET.Element(S + "hyperlinks")
        sheet.find(S + "tableParts").addprevious(links)
        # Freeze the identifier and pilot columns when scrolling the wide register.
        pane = sheet.find(".//" + S + "pane")
        pane.set("xSplit", "2")
        pane.set("topLeftCell", "C2")
        pane.set("activePane", "bottomRight")
        selection = sheet.find(".//" + S + "selection")
        if selection is not None:
            selection.set("pane", "bottomRight")
            selection.set("activeCell", "C2")
            selection.set("sqref", "C2")
        for i, row in enumerate(rows, 2):
            for col, key in zip(
                "IJKL", ["target_url", "actual_url", "period_url", "supporting_url"]
            ):
                if url := row[key]:
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
        updated = {
            SHEET: ET.tostring(sheet, encoding="utf-8"),
            RELS: ET.tostring(relationships, encoding="utf-8"),
        }
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
