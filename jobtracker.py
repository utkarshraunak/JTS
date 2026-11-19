"""Job Tracking System - core module (Utkarsh Raunak, 01914803124)."""
from dataclasses import dataclass, field
from datetime import date

# Application life-cycle (Finite State Machine)
STATUSES = ["Saved", "Applied", "Interview", "Offer", "Accepted", "Rejected", "Withdrawn"]
CLOSED = {"Accepted", "Rejected", "Withdrawn"}
TRANSITIONS = {
    "Saved": {"Applied", "Withdrawn"},
    "Applied": {"Interview", "Rejected", "Withdrawn"},
    "Interview": {"Offer", "Rejected", "Withdrawn"},
    "Offer": {"Accepted", "Rejected", "Withdrawn"},
    "Accepted": set(), "Rejected": set(), "Withdrawn": set(),
}


@dataclass
class Application:
    app_id: int
    company: str
    role: str
    deadline: date = None
    status: str = "Saved"
    notes: list = field(default_factory=list)


class JobTracker:
    def __init__(self):
        self._apps = {}          # O(1) hash index on app_id
        self._next = 1

    def add(self, company, role, deadline=None):
        if not company or not role:
            raise ValueError("company and role are required")
        a = Application(self._next, company, role, deadline)
        self._apps[a.app_id] = a
        self._next += 1
        return a

    def get(self, app_id):
        return self._apps[app_id]

    def update_status(self, app_id, new_status):
        a = self._apps[app_id]
        if new_status not in TRANSITIONS[a.status]:
            raise ValueError(f"Invalid transition {a.status} -> {new_status}")
        a.status = new_status
        return a

    def search(self, company=None, status=None):
        return [a for a in self._apps.values()
                if (company is None or company.lower() in a.company.lower())
                and (status is None or a.status == status)]

    def upcoming_deadlines(self, today, within_days=7):
        out = [a for a in self._apps.values()
               if a.status not in CLOSED and a.deadline is not None
               and 0 <= (a.deadline - today).days <= within_days]
        return sorted(out, key=lambda a: a.deadline)


def reminder_level(days_left, status):
    """Reminder priority used by the follow-up/deadline alert module."""
    if status in CLOSED:
        return "Closed"
    if days_left < 0:
        level = "Overdue"
    elif days_left <= 3:
        level = "Urgent"
    else:
        level = "Normal"
    return level


def reminder_level_faulty(days_left, status):
    """Seeded fault: day 3 is never assigned a level (use-without-definition)."""
    if status in CLOSED:
        return "Closed"
    if days_left < 0:
        level = "Overdue"
    elif days_left < 3:
        level = "Urgent"
    elif days_left > 3:
        level = "Normal"
    return level
