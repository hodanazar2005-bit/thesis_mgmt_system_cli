from datetime import datetime
from typing import List, Optional
from .db import get_db
from .models import Thesis
from .utils import sha256, next_id

def login_student(student_id: str, password: str):
    db = get_db()
    s = db.students.get(student_id)
    return s if s and s.password_hash == sha256(password) else None

def login_professor(professor_id: str, password: str):
    db = get_db()
    p = db.professors.get(professor_id)
    return p if p and p.password_hash == sha256(password) else None

def student_request_thesis(student_id, advisor_id, title, keywords, abstract):
    db = get_db()
    s = db.students[student_id]
    adv = db.professors[advisor_id]
    if len(adv.current_advisees) >= adv.capacity_advisor:
        raise ValueError("Advisor capacity full")
    thesis_id = next_id("T", db.theses.keys())
    thesis = Thesis(thesis_id, title, keywords, abstract, None, student_id, advisor_id,
                    year=s.year, semester=s.semester)
    db.theses[thesis_id] = thesis
    s.thesis_id, s.advisor_id, s.thesis_request_status = thesis_id, advisor_id, "requested"
    db.save()
    return thesis_id

def professor_review_requests(professor_id):
    db = get_db()
    return [s for s in db.students.values() if s.advisor_id==professor_id and s.thesis_request_status=="requested"]

def professor_approve_request(professor_id, student_id, approve: bool):
    db = get_db()
    s, p = db.students[student_id], db.professors[professor_id]
    if approve:
        if len(p.current_advisees) >= p.capacity_advisor:
            raise ValueError("Advisor capacity full")
        s.thesis_request_status = "approved"
        p.current_advisees.append(student_id)
    else:
        s.thesis_request_status = "rejected"
        s.advisor_id = None
        if s.thesis_id: 
            db.theses.pop(s.thesis_id, None)
            s.thesis_id = None
    db.save()

def assign_judges_and_schedule(professor_id, thesis_id, judge_internal_id, judge_external, defense_date):
    db = get_db()
    t = db.theses[thesis_id]
    if t.advisor_id != professor_id:
        raise PermissionError("Only advisor can assign judges")
    j = db.professors[judge_internal_id]
    if len(j.current_judgings) >= j.capacity_judge:
        raise ValueError("Internal judge capacity full")
    t.judge_internal_id, t.judge_external, t.defense_date, t.status = judge_internal_id, judge_external, defense_date, "scheduled"
    if thesis_id not in j.current_judgings:
        j.current_judgings.append(thesis_id)
    db.save()

def record_defense_result(professor_id, thesis_id, grade, result):
    db = get_db()
    t = db.theses[thesis_id]
    if t.advisor_id != professor_id:
        raise PermissionError("Only advisor can record grade")
    t.grade, t.result, t.status = grade, result, "defended"
    db.save()

def search_thesis_bank(query: str="", year:Optional[int]=None, advisor:Optional[str]=None):
    db = get_db()
    q = query.lower().strip()
    results = []
    for t in db.theses.values():
        if year and t.year!=year: continue
        adv = db.professors.get(t.advisor_id).name if t.advisor_id in db.professors else "-"
        stu = db.students.get(t.student_id).name if t.student_id in db.students else "-"
        text = " ".join([t.title," ".join(t.keywords),adv,stu]).lower()
        if advisor and advisor!=adv: continue
        if q and q not in text: continue
        results.append(f"[{t.thesis_id}] {t.title} — {stu} — Advisor: {adv} — Status: {t.status}")
    return results