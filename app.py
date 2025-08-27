from getpass import getpass
from core.services import *
from core.utils import prompt_nonempty
from core.db import get_db

def student_panel(sid):
    while True:
        print("\n[Student Menu]\n1) Request Thesis\n2) Check Status\n3) Search Theses\n0) Exit")
        c = input("Choice: ")
        if c=="1":
            pid=input("Advisor ID: "); title=prompt_nonempty("Title: ")
            kws=prompt_nonempty("Keywords(comma): ").split(",")
            abs=prompt_nonempty("Abstract: ")
            try:
                tid = student_request_thesis(sid,pid,title,[k.strip() for k in kws],abs)
                print("Created Thesis:", tid)
            except Exception as e:
                print("Error:", e)
        elif c=="2":
            s=get_db().students[sid]
            print(s.thesis_request_status,s.advisor_id,s.thesis_id)
        elif c=="3":
            q=input("Query: ")
            [print(r) for r in search_thesis_bank(q)]
        elif c=="0": break

def professor_panel(pid):
    while True:
        print("\n[Professor Menu]\n1) Review Requests\n2) Assign Judges\n3) Record Grade\n4) Search Theses\n0) Exit")
        c=input("Choice: ")
        if c=="1":
            reqs=professor_review_requests(pid); [print(s.student_id,s.name) for s in reqs]
            if reqs:
                sid=input("Student ID:")
                approve=input("Approve? (y/n): ").lower()=="y"
                professor_approve_request(pid,sid,approve)
        elif c=="2":
            tid=input("Thesis ID: "); jid=input("Internal Judge ID: "); jext=input("External Judge: "); d=input("Date:")
            try:
                assign_judges_and_schedule(pid,tid,jid,jext,d)
            except Exception as e:
                print("Error:", e)
        elif c=="3":
            tid=input("Thesis ID: "); g=input("Grade: "); r=input("Result: ")
            record_defense_result(pid,tid,g,r)
        elif c=="4":
            [print(r) for r in search_thesis_bank(input("Query: "))]
        elif c=="0": break

def main():
    get_db()
    while True:
        print("\n1) Student\n2) Professor\n3) Search Theses\n0) Exit")
        c=input("Choice: ")
        if c=="1":
            sid=input("ID: "); pwd=getpass("Password: ")
            if login_student(sid,pwd): student_panel(sid)
            else: print("Login failed.")
        elif c=="2":
            pid=input("ID: "); pwd=getpass("Password: ")
            if login_professor(pid,pwd): professor_panel(pid)
            else: print("Login failed.")
        elif c=="3":
            [print(r) for r in search_thesis_bank(input("Query: "))]
        elif c=="0": break

if __name__ == "__main__":
    main()