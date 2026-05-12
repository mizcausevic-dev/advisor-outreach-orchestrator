from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.outreach_service import build_service


class OutreachServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = build_service(ROOT)

    def test_summary_shape(self) -> None:
        summary = self.service.summary()
        self.assertEqual(summary["institution"], "Northstar Online University")
        self.assertGreater(summary["studentCount"], 0)

    def test_queue_prioritizes_financial_hold_and_reply_drift(self) -> None:
        queue = self.service.outreach_queue()
        self.assertEqual(queue[0]["studentId"], "stu-1880")

    def test_student_lookup(self) -> None:
        student = self.service.student("stu-2041")
        self.assertIsNotNone(student)
        self.assertEqual(student["leadChannel"], "sms")


if __name__ == "__main__":
    unittest.main()
