"""Đọc hai bản trả riêng của P5-V1. Chỉ tính chỉ số sau khi đủ cả hai phiếu."""
import argparse
from datetime import datetime
import json
from pathlib import Path
from statistics import mean, median

from openpyxl import load_workbook

HERE = Path(__file__).resolve().parent
SPEC = json.loads((HERE / "ho_so.json").read_text(encoding="utf-8"))
DECISIONS = {"Duyệt", "Không duyệt"}
PUBLIC_RESULT = Path("results/pilot5_review.json")
PRIVATE_BALLOTS = HERE.parent / "du_lieu/phieu_pilot5"


def read_ballot(path, person):
    book = load_workbook(path)
    rows = {}
    previous = None
    try:
        if book["Huong dan"]["A1"].value != "Pilot 5    |    Phiếu độc lập " + person:
            raise ValueError("Sai danh tính phiếu " + person)
        for index, (mode, cases) in enumerate(SPEC[person], 1):
            sheet = book["Luot " + str(index)]
            expected_title = "Đánh giá thông thường" if mode == "A" else "Đánh giá có checklist"
            if sheet["A1"].value != f"{person}    |    Lượt {index}    |    {expected_title}":
                raise ValueError(f"Sai điều kiện {person} lượt {index}")
            for n, key in enumerate(cases, 6):
                cells = sheet[n]
                if [c.value for c in cells[:4]] != [key, *SPEC["cases"][key]]:
                    raise ValueError(f"Sai hồ sơ hoặc tiêu chí {person} {key}")
                inputs = [*cells[4:6], *cells[7:9]]
                if mode == "B":
                    inputs.extend(cells[9:12])
                if all(c.value is None for c in inputs):
                    continue
                if any(c.data_type == "f" for c in inputs):
                    raise ValueError(f"{person} {key}: cần giá trị tĩnh.")
                start, finish, choice, note, *checks = [c.value for c in inputs]
                if not isinstance(start, datetime) or not isinstance(finish, datetime) or finish <= start:
                    raise ValueError(f"{person} {key}: cần ngày giờ bắt đầu và kết thúc hợp lệ.")
                if previous and start < previous:
                    raise ValueError(f"{person} {key}: giờ chấm chồng lấn hoặc đảo thứ tự.")
                if choice not in DECISIONS or not isinstance(note, str) or not note.strip():
                    raise ValueError(f"{person} {key}: thiếu quyết định hoặc căn cứ.")
                if any(value not in {"Có", "Không"} for value in checks):
                    raise ValueError(f"{person} {key}: thiếu câu trả lời checklist.")
                elapsed = round((finish - start).total_seconds())
                if elapsed < 1:
                    raise ValueError(f"{person} {key}: thời gian dưới một giây.")
                rows[key] = (mode, choice == "Duyệt", elapsed)
                previous = finish
    finally:
        book.close()
    return rows


def summarize(p1, p2):
    votes = {person: read_ballot(path, person) for person, path in zip(("P1", "P2"), (p1, p2))}
    count = sum(map(len, votes.values()))
    state = {"received_complete_ballots": sum(len(v) == 6 for v in votes.values()),
             "valid_decisions": count, "expected_decisions": 12,
             "missing": {p: sorted(SPEC["cases"].keys() - v.keys()) for p, v in votes.items()}}
    if count != 12:
        return dict(state, status="Chờ đủ hai phiếu", comparison=None)
    run = json.loads((HERE / "phep_do.json").read_text(encoding="utf-8"))
    rows = run["exceptions"]
    targets = {"R1": len(run["files"]) == 12,
               "R2": all(r["frozen_reference_matched"] == 1809 for r in rows),
               "R3": run["matched"] == run["denominator"] == 180900,
               "R4": False,  # D6.3 p.53 describes availability; no five-level UI record.
               "R5": len(rows) == 9 and all(r["adjusted_pillars_matched"] == 1809
                                           and r["adjusted_total_matched"] == 603 for r in rows),
               "R6": False}  # The five official optimizer outputs are still missing.
    metrics = {}
    for mode in ("A", "B"):
        obs = [(approved, seconds, targets[k]) for v in votes.values()
               for k, (m, approved, seconds) in v.items() if m == mode]
        times = [s for _, s, _ in obs]
        metrics[mode] = {"cases": len(obs), "correct": sum(a == ref for a, _, ref in obs),
                         "false_approvals": sum(a and not ref for a, _, ref in obs),
                         "reference_negative": sum(not ref for _, _, ref in obs),
                         "false_rejections": sum(not a and ref for a, _, ref in obs),
                         "reference_positive": sum(ref for _, _, ref in obs),
                         "mean_seconds": mean(times), "median_seconds": median(times)}
    conflicts = [k for k in targets if votes["P1"][k][1] != votes["P2"][k][1]]
    return dict(state, status="Đủ hai phiếu, chờ PM xét căn cứ và ký",
                comparison=metrics, agreements=6-len(conflicts), disagreement_ids=conflicts)


def report_review(directory=None):
    """Prefer submitted ballots. A public checkout reproduces the released aggregate."""
    released = json.loads((HERE.parent / PUBLIC_RESULT).read_text(encoding="utf-8"))
    folder = PRIVATE_BALLOTS if directory is None else directory
    returns = [folder / f"{person}.xlsx" for person in ("P1", "P2")]
    has_returns = any(path.exists() for path in returns)
    if directory is not None and not has_returns:
        raise ValueError(f"Không tìm thấy P1.xlsx hoặc P2.xlsx trong {directory}")
    paths = [path if path.exists() else HERE / path.name for path in returns]
    current = summarize(*paths)
    if not has_returns and not current["valid_decisions"]:
        return released
    for person, missing in current["missing"].items():
        if set(missing) - set(released["missing"][person]):
            raise ValueError(f"Thiếu quyết định {person} đã công bố. Kiểm tra lại các phiếu đầu vào.")
    return current


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("p1", type=Path)
    parser.add_argument("p2", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(summarize(args.p1, args.p2), indent=2, ensure_ascii=False))
    except (KeyError, ValueError) as error:
        parser.exit(2, str(error) + "\n")
