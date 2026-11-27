"""Compare conditional D6.4 handover dates using the published version history."""

import argparse
import csv
import io
from datetime import date, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = "http://schemas.microsoft.com/project"
ET.register_namespace("", NS)
P = "{" + NS + "}"
CSV_PATH = ROOT / "results/d64_review_scenarios.csv"
XML_PATH = ROOT / "results/D6_4_kich_ban_ProjectLibre.xml"


def observed_schedule():
    project = ET.parse(ROOT / "FAME_Lich_MS_Project.xml").getroot()
    tasks = {t.findtext(P + "UID"): t for t in project.find(P + "Tasks")}

    def day(uid, tag):
        return date.fromisoformat(tasks[uid].findtext(P + tag).split("T")[0])

    ready, feedback, handover = (day(uid, "ActualFinish") for uid in ("15", "16", "17"))
    return (
        ready,
        feedback,
        handover,
        day("17", "Deadline"),
        tasks["17"].findtext(P + "HyperlinkAddress"),
    )


def scenarios(wait_days=7, backup_days=2):
    if wait_days < 0 or backup_days < 0:
        raise ValueError("Waiting times must be nonnegative calendar days")
    ready, feedback, handover, deadline, source = observed_schedule()
    rows = []
    for code, label, wait in [
        ("S0", "Tham chiếu lịch sử", 0),
        ("S1", "Chờ người phản biện", wait_days),
        ("S2", "Có người dự phòng", min(backup_days, wait_days)),
    ]:
        new_finish = handover + timedelta(days=wait)
        rows.append(
            dict(
                case=code,
                label=label,
                wait_days=wait,
                ready=ready.isoformat(),
                feedback=(feedback + timedelta(days=wait)).isoformat(),
                finish=new_finish.isoformat(),
                due=deadline.isoformat(),
                versus_observed_days=(new_finish - handover).days,
                versus_cover_days=(new_finish - deadline).days,
                cover_source=source,
                history_source=source.replace("#page=1", "#page=2"),
            )
        )
    return rows


def scenario_xml(rows):
    # Reuse the historical 7-day calendar; each 8-hour working interval is one calendar day.
    calendar = (
        ET.parse(ROOT / "FAME_Lich_MS_Project.xml").getroot().find(P + "Calendars")
    )
    root = ET.Element(P + "Project")

    def fields(parent, **items):
        for key, value in items.items():
            ET.SubElement(parent, P + key).text = str(value)

    def at(day):
        return day + "T10:00:00"

    fields(
        root,
        SaveVersion=14,
        Name="D6.4 | Mô phỏng phản biện của người viết",
        ScheduleFromStart=1,
        StartDate=at(rows[0]["ready"]),
        FinishDate=at(max(r["finish"] for r in rows)),
        CalendarUID=1,
        DefaultStartTime="08:00:00",
        DefaultFinishTime="17:00:00",
        MinutesPerDay=480,
        MinutesPerWeek=3360,
        DaysPerMonth=30,
    )
    root.append(calendar)
    tasks = ET.SubElement(root, P + "Tasks")
    labels = (
        ("ready", "Bản sẵn sàng phản biện"),
        ("feedback", "Nhận ý kiến"),
        ("finish", "Bàn giao"),
    )
    for group, row in enumerate(rows):
        first = 4 * group + 1
        summary = ET.SubElement(tasks, P + "Task")
        span = (
            date.fromisoformat(row["finish"]) - date.fromisoformat(row["ready"])
        ).days
        fields(
            summary,
            UID=first,
            ID=first,
            Name=row["case"] + " | " + row["label"],
            Type=1,
            IsNull=0,
            WBS=group + 1,
            OutlineNumber=group + 1,
            OutlineLevel=1,
            Start=at(row["ready"]),
            Finish=at(row["finish"]),
            Duration=f"PT{span * 8}H0M0S",
            DurationFormat=7,
            Summary=1,
        )
        for index, (key, label) in enumerate(labels, 1):
            uid = first + index
            task = ET.SubElement(tasks, P + "Task")
            fields(
                task,
                UID=uid,
                ID=uid,
                Name=row["case"] + " | " + label,
                Type=1,
                IsNull=0,
                WBS=f"{group + 1}.{index}",
                OutlineNumber=f"{group + 1}.{index}",
                OutlineLevel=2,
                Start=at(row[key]),
                Finish=at(row[key]),
                Duration="PT0H0M0S",
                DurationFormat=7,
                Milestone=1,
                Summary=0,
            )
            if index == 1:
                fields(task, ConstraintType=2, ConstraintDate=at(row[key]))
            fields(
                task,
                Notes=f"{row['label']}. S0 dùng lịch sử phiên bản. S1/S2 là kịch bản của người viết. {row['history_source']}",
            )
            if index > 1:
                prior = labels[index - 2][0]
                lag = (
                    date.fromisoformat(row[key]) - date.fromisoformat(row[prior])
                ).days
                link = ET.SubElement(task, P + "PredecessorLink")
                fields(
                    link,
                    PredecessorUID=uid - 1,
                    Type=1,
                    LinkLag=lag * 4800,
                    LagFormat=7,
                )
    ET.indent(root)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument(
        "--check", action="store_true", help="Verify the published scenarios (default)"
    )
    args = parser.parse_args()
    rows = scenarios()
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    for path, content in [
        (CSV_PATH, buf.getvalue().encode()),
        (XML_PATH, scenario_xml(rows)),
    ]:
        if args.write:
            path.write_bytes(content)
        elif path.read_bytes() != content:
            raise ValueError(
                f"Scenario output differs from version history and assumptions: {path.name}"
            )
    print("D6.4:", ", ".join(row["case"] + " " + row["finish"] for row in rows))


if __name__ == "__main__":
    main()
