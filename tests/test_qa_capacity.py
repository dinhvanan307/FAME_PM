from collections import Counter
from datetime import date
import unittest
from xml.etree import ElementTree as ET

from fame_pm.qa_capacity import P, daily_load, make_jobs, metrics, project_xml


class QACapacityTests(unittest.TestCase):
    def test_added_reviewer_changes_capacity_not_total_effort(self):
        jobs = make_jobs()
        rows = daily_load(jobs)
        for view in ("nhu_cau", "can_tai"):
            work = Counter()
            for row in rows:
                if row["view"] == view:
                    work[row["plan"]] += row["work_h"]
            self.assertEqual(work, {"A": 24, "B": 24})
        self.assertEqual(
            metrics(jobs),
            {
                "A": dict(
                    request_excess=16,
                    feasible_excess=0,
                    last=date(2025, 8, 4),
                    on_target=1,
                ),
                "B": dict(
                    request_excess=8,
                    feasible_excess=0,
                    last=date(2025, 8, 1),
                    on_target=2,
                ),
            },
        )

    def test_projects_keep_alternatives_separate_and_match_each_job(self):
        jobs = make_jobs()
        for view in ("nhu_cau", "can_tai"):
            root = ET.fromstring(project_xml(jobs, view))
            resources = {
                r.findtext(P + "UID"): r.findtext(P + "Name")
                for r in root.find(P + "Resources")
            }
            assignments = {
                a.findtext(P + "TaskUID"): a.findtext(P + "ResourceUID")
                for a in root.find(P + "Assignments")
            }
            by_reviewer = {}
            tasks = root.find(P + "Tasks")
            self.assertEqual(len(tasks), 6)
            for task, job in zip(tasks, jobs):
                uid = task.findtext(P + "UID")
                reviewer = resources[assignments[uid]]
                self.assertEqual(reviewer, f"{job.plan} · {job.reviewer}")
                self.assertEqual(task.findtext(P + "HyperlinkAddress"), job.source)
                expected_day = job.target if view == "nhu_cau" else job.finish
                self.assertEqual(
                    task.findtext(P + "Finish"), f"{expected_day}T17:00:00"
                )
                predecessor = task.findtext(
                    P + "PredecessorLink/" + P + "PredecessorUID"
                )
                self.assertEqual(
                    predecessor,
                    by_reviewer.get(reviewer) if view == "can_tai" else None,
                )
                by_reviewer[reviewer] = uid
