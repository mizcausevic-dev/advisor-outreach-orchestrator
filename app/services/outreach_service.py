from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any


def _clamp(value: float, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, round(value)))


@dataclass(slots=True)
class AdvisorOutreachService:
    source_path: Path

    def load(self) -> dict[str, Any]:
        return json.loads(self.source_path.read_text(encoding="utf-8"))

    def score_student(self, student: dict[str, Any]) -> dict[str, Any]:
        attendance = student["attendance_trend"] * 100
        assignments = student["assignment_completion_rate"] * 100
        response_penalty = student["days_since_last_reply"] * 1.7
        attempt_penalty = student["advisor_attempts"] * 2.1
        no_show_penalty = student["no_show_history"] * 3.2
        faculty_penalty = 8 if student["faculty_concern"] else 0
        finance_penalty = 12 if student["financial_hold"] else 0
        band_penalty = {"stable": 0, "watch": 7, "high": 12}[student["risk_band"]]

        urgency_score = _clamp(
            100
            - (attendance * 0.34 + assignments * 0.37)
            + response_penalty
            + attempt_penalty
            + no_show_penalty
            + faculty_penalty
            + finance_penalty
            + band_penalty
        )

        status = "escalate" if urgency_score >= 76 else "priority" if urgency_score >= 50 else "monitor"
        lead_channel = self._lead_channel(student, status)
        owner_lane = self._owner_lane(student, status)
        playbook = self._playbook(student, status, lead_channel, owner_lane)

        return {
            "studentId": student["student_id"],
            "name": student["name"],
            "program": student["program"],
            "cohort": student["cohort"],
            "urgencyScore": urgency_score,
            "status": status,
            "leadChannel": lead_channel,
            "ownerLane": owner_lane,
            "daysSinceLastReply": student["days_since_last_reply"],
            "advisorAttempts": student["advisor_attempts"],
            "attendanceTrend": round(attendance, 1),
            "assignmentCompletionRate": round(assignments, 1),
            "financialHold": student["financial_hold"],
            "facultyConcern": student["faculty_concern"],
            "nextAction": playbook["nextAction"],
            "playbookSteps": playbook["steps"],
        }

    def _lead_channel(self, student: dict[str, Any], status: str) -> str:
        if student["financial_hold"]:
            return "phone"
        if status == "escalate" and student["sms_opt_in"]:
            return "sms"
        return student["preferred_channel"]

    def _owner_lane(self, student: dict[str, Any], status: str) -> str:
        if student["financial_hold"]:
            return "Financial Support"
        if student["faculty_concern"] and status != "monitor":
            return "Faculty + Advising"
        if status == "escalate":
            return "Care Team"
        return "Advising"

    def _playbook(
        self,
        student: dict[str, Any],
        status: str,
        lead_channel: str,
        owner_lane: str,
    ) -> dict[str, Any]:
        if status == "escalate":
            next_action = (
                f"Launch a {lead_channel} outreach now, then route the case into {owner_lane} "
                "with a same-week checkpoint and faculty context attached."
            )
            steps = [
                f"Send {lead_channel} outreach inside one business day.",
                "Attach attendance and assignment drift summary for context.",
                "Escalate to owner lane if no response after two business days.",
            ]
        elif status == "priority":
            next_action = (
                f"Queue a {lead_channel} touch this week and keep the case with {owner_lane} "
                "unless momentum drops again."
            )
            steps = [
                f"Send {lead_channel} outreach this week.",
                "Offer tutoring, planning, or schedule support based on the student's blockers.",
                "Re-score the case after the next assignment window.",
            ]
        else:
            next_action = (
                f"Keep the student in a light-touch {lead_channel} reminder lane and watch for "
                "response or assignment drift before escalating."
            )
            steps = [
                f"Send a low-friction {lead_channel} check-in.",
                "Hold the case in monitor status for the next seven days.",
                "Promote to priority only if another signal slips.",
            ]
        return {"nextAction": next_action, "steps": steps}

    def scored_students(self) -> list[dict[str, Any]]:
        data = self.load()
        return sorted(
            [self.score_student(student) for student in data["students"]],
            key=lambda item: (-item["urgencyScore"], item["name"]),
        )

    def summary(self) -> dict[str, Any]:
        data = self.load()
        scored = self.scored_students()
        escalations = [student for student in scored if student["status"] == "escalate"]
        priorities = [student for student in scored if student["status"] == "priority"]
        finance = [student for student in scored if student["financialHold"]]
        avg_urgency = mean(student["urgencyScore"] for student in scored)
        return {
            "institution": data["institution"],
            "term": data["term"],
            "studentCount": len(scored),
            "escalationCount": len(escalations),
            "priorityCount": len(priorities),
            "financialHoldCount": len(finance),
            "averageUrgencyScore": round(avg_urgency, 1),
            "topLane": scored[0]["ownerLane"],
            "leadRecommendation": (
                "Separate financial-hold cases from general advising drift, then reserve the care team lane "
                "for students with both silence and repeated missed commitments."
            ),
        }

    def outreach_queue(self) -> list[dict[str, Any]]:
        return self.scored_students()

    def lane_breakdown(self) -> list[dict[str, Any]]:
        lanes: dict[str, int] = {}
        for student in self.scored_students():
            lanes[student["ownerLane"]] = lanes.get(student["ownerLane"], 0) + 1
        return [{"ownerLane": lane, "count": count} for lane, count in sorted(lanes.items())]

    def playbooks(self) -> list[dict[str, Any]]:
        return [
            {
                "studentId": student["studentId"],
                "name": student["name"],
                "status": student["status"],
                "ownerLane": student["ownerLane"],
                "leadChannel": student["leadChannel"],
                "steps": student["playbookSteps"],
            }
            for student in self.scored_students()
        ]

    def student(self, student_id: str) -> dict[str, Any] | None:
        for student in self.scored_students():
            if student["studentId"] == student_id:
                return student
        return None

    def sample_payload(self) -> dict[str, Any]:
        queue = self.outreach_queue()
        return {
            "dashboard": self.summary(),
            "outreachQueue": [
                {
                    "studentId": student["studentId"],
                    "name": student["name"],
                    "urgencyScore": student["urgencyScore"],
                    "ownerLane": student["ownerLane"],
                    "leadChannel": student["leadChannel"],
                    "nextAction": student["nextAction"],
                }
                for student in queue[:3]
            ],
        }


def build_service(root: Path | None = None) -> AdvisorOutreachService:
    base = root or Path(__file__).resolve().parents[2]
    return AdvisorOutreachService(base / "app" / "data" / "sample_outreach.json")
