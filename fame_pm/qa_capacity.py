"""Build the QA demand and capacity-constrained schedules for the July handovers."""

import argparse
import csv
import io
from collections import Counter
from dataclasses import dataclass
from datetime import date, timedelta
from xml.etree import ElementTree as ET

from fame_pm.review_scenario import P, ROOT

FOLDER = ROOT / "results/qa"
CODES = ("D2.4", "D3.5", "D3.6")
HOURS = 8  # One complete, indivisible QA shift per dossier and per reviewer-day.
PLANS = {"A": ("QA chính",), "B": ("QA chính", "QA hỗ trợ")}
VIEWS = {"nhu_cau": "Nhu cầu giao cùng ngày", "can_tai": "Lịch giao theo năng lực"}


@dataclass(frozen=True)
class Job:
    code: str
    plan: str
    reviewer: str
    target: date
    finish: date
    source: str


def make_jobs():
    with (ROOT / "evidence/deliverables.csv").open(
        encoding="utf-8", newline=""
    ) as source:
        covers = {r["deliverable"]: r for r in csv.DictReader(source)}
    dates = {date.fromisoformat(covers[code]["delivered"]) for code in CODES}
    if len(dates) != 1:
        raise ValueError("The three source covers must identify the same handover day")
    target = dates.pop()
    if target.weekday() >= 5:
        raise ValueError("This scenario assumes a weekday release")
    jobs = []
    for plan, team in PLANS.items():
        available = dict.fromkeys(team, target)
        for code in CODES:
            reviewer = min(team, key=available.get)
            finish = available[reviewer]
            following = finish + timedelta(days=1)
            while following.weekday() >= 5:
                following += timedelta(days=1)
            available[reviewer] = following
            jobs.append(
                Job(code, plan, reviewer, target, finish, covers[code]["source_url"])
            )
    return jobs


def work_day(view, job):
    return job.target if view == "nhu_cau" else job.finish


def daily_load(jobs):
    rows = []
    for view in VIEWS:
        for plan, team in PLANS.items():
            assigned = Counter(
                (work_day(view, j), j.reviewer) for j in jobs if j.plan == plan
            )
            day = min(day for day, _ in assigned)
            end = max(day for day, _ in assigned)
            while day <= end:
                if day.weekday() < 5:
                    for name in team:
                        hours = HOURS * assigned[day, name]
                        rows.append(
                            dict(
                                view=view,
                                plan=plan,
                                date=day,
                                reviewer=name,
                                work_h=hours,
                                capacity_h=HOURS,
                                excess_h=max(0, hours - HOURS),
                            )
                        )
                day += timedelta(days=1)
    return rows


def metrics(jobs):
    daily = daily_load(jobs)
    return {
        plan: dict(
            request_excess=sum(
                r["excess_h"]
                for r in daily
                if r["plan"] == plan and r["view"] == "nhu_cau"
            ),
            feasible_excess=sum(
                r["excess_h"]
                for r in daily
                if r["plan"] == plan and r["view"] == "can_tai"
            ),
            last=max(j.finish for j in jobs if j.plan == plan),
            on_target=sum(j.finish == j.target for j in jobs if j.plan == plan),
        )
        for plan in PLANS
    }


def put(parent, tag, **fields):
    element = ET.SubElement(parent, P + tag)
    for key, value in fields.items():
        ET.SubElement(element, P + key).text = str(value)
    return element


def stamp(day, hour):
    return f"{day}T{hour:02d}:00:00"


def project_xml(jobs, view):
    root = ET.Element(P + "Project")
    name = "Mô phỏng QA | " + VIEWS[view]
    for key, value in dict(
        SaveVersion=14,
        Name=name,
        ScheduleFromStart=1,
        StartDate=stamp(jobs[0].target, 8),
        FinishDate=stamp(max(work_day(view, j) for j in jobs), 17),
        CalendarUID=1,
        DefaultStartTime="08:00:00",
        DefaultFinishTime="17:00:00",
        MinutesPerDay=480,
        MinutesPerWeek=2400,
        DaysPerMonth=20,
    ).items():
        ET.SubElement(root, P + key).text = str(value)
    calendars = put(root, "Calendars")
    weekdays = put(
        put(
            calendars,
            "Calendar",
            UID=1,
            Name="QA T2–T6, 8 giờ",
            IsBaseCalendar=1,
            BaseCalendarUID=-1,
        ),
        "WeekDays",
    )
    for day_type in range(1, 8):
        working = day_type not in (1, 7)
        weekday = put(weekdays, "WeekDay", DayType=day_type, DayWorking=int(working))
        if working:
            periods = put(weekday, "WorkingTimes")
            for begin, end in ((8, 12), (13, 17)):
                put(
                    periods,
                    "WorkingTime",
                    FromTime=f"{begin:02d}:00:00",
                    ToTime=f"{end:02d}:00:00",
                )

    tasks, resources, assignments = (
        put(root, tag) for tag in ("Tasks", "Resources", "Assignments")
    )
    ids = {}
    for plan, team in PLANS.items():
        for reviewer in team:
            uid = len(ids) + 1
            ids[plan, reviewer] = uid
            name = f"{plan} · {reviewer}"
            put(
                calendars,
                "Calendar",
                UID=uid + 1,
                Name=name,
                IsBaseCalendar=0,
                BaseCalendarUID=1,
            )
            put(
                resources,
                "Resource",
                UID=uid,
                ID=uid,
                Name=name,
                Type=1,
                IsNull=0,
                MaxUnits=1,
                CanLevel=1,
                CalendarUID=uid + 1,
            )
    previous = {}
    for uid, job in enumerate(jobs, 1):
        day = work_day(view, job)
        start, finish = stamp(day, 8), stamp(day, 17)
        rid = ids[job.plan, job.reviewer]
        duration = f"PT{HOURS}H0M0S"
        task = put(
            tasks,
            "Task",
            UID=uid,
            ID=uid,
            Name=f"{job.plan} · {job.code} · kiểm QA và giao",
            Type=1,
            IsNull=0,
            OutlineNumber=uid,
            OutlineLevel=1,
            Start=start,
            Finish=finish,
            Duration=duration,
            DurationFormat=7,
            Work=duration,
            EffortDriven=0,
            Milestone=0,
            Summary=0,
            ConstraintType=0,
            CalendarUID=-1,
            Deadline=stamp(job.target, 17),
            Notes=f"Giả định mỗi hồ sơ cần {HOURS} giờ, giao ngay khi xong QA. Ngày giao trên bìa: {job.target}.",
            Hyperlink=job.code + " · bìa FAME",
            HyperlinkAddress=job.source,
        )
        if view == "can_tai" and rid in previous:
            put(
                task,
                "PredecessorLink",
                PredecessorUID=previous[rid],
                Type=1,
                LinkLag=0,
                LagFormat=7,
            )
        previous[rid] = uid
        put(
            assignments,
            "Assignment",
            UID=uid,
            TaskUID=uid,
            ResourceUID=rid,
            PercentWorkComplete=0,
            Finish=finish,
            RegularWork=duration,
            RemainingWork=duration,
            Start=start,
            Units=1,
            Work=duration,
            WorkContour=0,
        )
    ET.indent(root)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


def as_csv(rows):
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument(
        "--check",
        action="store_true",
        help="Compare generated results with the release (default)",
    )
    args = parser.parse_args()
    jobs = make_jobs()
    handovers = [
        dict(
            plan=j.plan,
            code=j.code,
            reviewer=j.reviewer,
            assumed_work_h=HOURS,
            cover_delivered=j.target,
            requested=j.target,
            feasible=j.finish,
            calendar_days_after_target=(j.finish - j.target).days,
            cover_source=j.source,
        )
        for j in jobs
    ]
    files = {
        "lich_giao.csv": as_csv(handovers),
        "tai_theo_ngay.csv": as_csv(daily_load(jobs)),
    }
    for view in VIEWS:
        files[view + ".xml"] = project_xml(jobs, view)
    for name, content in files.items():
        path = FOLDER / name
        if args.write:
            FOLDER.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        elif path.read_bytes() != content:
            raise ValueError(f"Stale QA output: {name}")
    for plan, stats in metrics(jobs).items():
        print(
            f"{plan}: request +{stats['request_excess']}h, feasible +{stats['feasible_excess']}h, last {stats['last']}"
        )


if __name__ == "__main__":
    main()
