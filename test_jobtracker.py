import unittest
from datetime import date
from jobtracker import JobTracker, reminder_level, reminder_level_faulty


class TestJobTracker(unittest.TestCase):
    def setUp(self):
        self.t = JobTracker()
        self.a = self.t.add("Google", "SDE Intern", date(2026, 12, 1))

    def test_1_add_and_get(self):
        self.assertEqual(self.t.get(self.a.app_id).company, "Google")
        self.assertEqual(self.a.status, "Saved")

    def test_2_missing_fields_rejected(self):
        with self.assertRaises(ValueError):
            self.t.add("", "Analyst")

    def test_3_valid_transitions(self):
        for s in ["Applied", "Interview", "Offer", "Accepted"]:
            self.t.update_status(self.a.app_id, s)
        self.assertEqual(self.a.status, "Accepted")

    def test_4_invalid_transition(self):
        with self.assertRaises(ValueError):
            self.t.update_status(self.a.app_id, "Offer")

    def test_5_closed_is_final(self):
        self.t.update_status(self.a.app_id, "Withdrawn")
        with self.assertRaises(ValueError):
            self.t.update_status(self.a.app_id, "Applied")

    def test_6_search_filters(self):
        self.t.add("Amazon", "Analyst")
        self.assertEqual(len(self.t.search(company="goo")), 1)
        self.assertEqual(len(self.t.search(status="Saved")), 2)

    def test_7_upcoming_deadlines_sorted(self):
        self.t.add("TCS", "Trainee", date(2026, 11, 22))
        res = self.t.upcoming_deadlines(date(2026, 11, 20), 7)
        self.assertEqual([r.company for r in res], ["TCS"])

    def test_8_reminder_levels(self):
        self.assertEqual(reminder_level(-1, "Applied"), "Overdue")
        self.assertEqual(reminder_level(3, "Saved"), "Urgent")
        self.assertEqual(reminder_level(9, "Saved"), "Normal")
        self.assertEqual(reminder_level(2, "Offer" if False else "Rejected"), "Closed")


if __name__ == "__main__":
    unittest.main()
