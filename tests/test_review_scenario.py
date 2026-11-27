import csv
import unittest
from datetime import date
from xml.etree import ElementTree as ET

from fame_pm.review_scenario import CSV_PATH, XML_PATH, P, scenarios


class ReviewScenarioTests(unittest.TestCase):
    def test_earliest_available_reviewer_wins(self):
        self.assertEqual(scenarios(7, 10)[1]["finish"], scenarios(7, 10)[2]["finish"])
        for row in scenarios(0, 2):
            self.assertEqual(row["finish"], "2025-02-20")
        self.assertEqual(scenarios(7, 0)[2]["finish"], scenarios()[0]["finish"])

    def test_project_milestones_match_the_published_run(self):
        root = ET.parse(XML_PATH).getroot()
        with CSV_PATH.open(encoding="utf-8", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(
            [r["finish"] for r in rows], ["2025-02-20", "2025-02-27", "2025-02-22"]
        )
        tasks = root.find(P + "Tasks").findall(P + "Task")
        self.assertEqual(len(tasks), 12)
        for i, row in enumerate(rows):
            previous_date = None
            for key, task in zip(
                ("ready", "feedback", "finish"), tasks[4 * i + 1 : 4 * i + 4]
            ):
                when = date.fromisoformat(row[key])
                self.assertEqual(task.findtext(P + "Finish")[:10], when.isoformat())
                self.assertIsNone(task.find(P + "ActualFinish"))
                if previous_date is not None:
                    link = task.find(P + "PredecessorLink")
                    self.assertEqual(
                        int(link.findtext(P + "PredecessorUID")),
                        int(task.findtext(P + "UID")) - 1,
                    )
                    self.assertEqual(
                        int(link.findtext(P + "LinkLag")),
                        (when - previous_date).days * 4800,
                    )
                previous_date = when
