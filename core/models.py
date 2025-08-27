from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Student:
    student_id: str
    name: str
    year: int
    semester: str
    password_hash: str
    advisor_id: Optional[str] = None
    thesis_id: Optional[str] = None
    thesis_request_status: str = "none"   # none, requested, approved, rejected

@dataclass
class Professor:
    professor_id: str
    name: str
    password_hash: str
    capacity_advisor: int
    capacity_judge: int
    fields: List[str]
    current_advisees: List[str] = field(default_factory=list)
    current_judgings: List[str] = field(default_factory=list)

@dataclass
class Thesis:
    thesis_id: str
    title: str
    keywords: List[str]
    abstract: str
    fulltext_link: Optional[str]
    student_id: str
    advisor_id: str
    year: int
    semester: str
    judge_internal_id: Optional[str] = None
    judge_external: Optional[str] = None
    defense_date: Optional[str] = None
    status: str = "draft"   # draft, scheduled, defended
    grade: Optional[str] = None
    result: Optional[str] = None