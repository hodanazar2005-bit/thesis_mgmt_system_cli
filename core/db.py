import os
from .store import load_json, save_json
from .models import Student, Professor, Thesis
from .utils import sha256

class DB:
    def init(self):
        self.students = {}
        self.professors = {}
        self.theses = {}

    def load(self):
        self.students = {x["student_id"]: Student(**x) for x in load_json("students.json", [])}
        self.professors = {x["professor_id"]: Professor(**x) for x in load_json("professors.json", [])}
        self.theses = {x["thesis_id"]: Thesis(**x) for x in load_json("theses.json", [])}

    def save(self):
        save_json("students.json", [vars(s) for s in self.students.values()])
        save_json("professors.json", [vars(p) for p in self.professors.values()])
        save_json("theses.json", [vars(t) for t in self.theses.values()])

    def ensure_seed(self):
        if not self.students and not self.professors:
            s1 = Student("40110001","Alice",2024,"First",sha256("1234"))
            s2 = Student("40110002","Bob",2024,"First",sha256("1234"))
            p1 = Professor("9001","Prof. Smith",sha256("admin1"),5,10,["AI","IR"])
            p2 = Professor("9002","Prof. Johnson",sha256("admin2"),5,10,["DB","Software"])
            self.students = {s1.student_id: s1, s2.student_id: s2}
            self.professors = {p1.professor_id: p1, p2.professor_id: p2}
            self.save()

db_instance = None
def get_db() -> DB:
    global db_instance
    if db_instance is None:
        db_instance = DB()
        db_instance.load()
        db_instance.ensure_seed()
    return db_instance