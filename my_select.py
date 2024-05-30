from pprint import pprint
import random
from sqlalchemy import Float, func
from database.models import Student, Group, Teacher, Subject, Grade
from database.db import DBSession, check_connection
from sqlalchemy import cast
from database.repository import get_all_teachers,\
                                get_all_students,\
                                get_all_subjects,\
                                get_all_groups


def select_random_teacher(session):
    all_teachers = get_all_teachers(session)
    random_teacher = random.choice(all_teachers)
    return random_teacher.name


def select_random_student(session):
    all_students = get_all_students(session)
    random_student = random.choice(all_students)
    return random_student.name


def select_random_group(session):
    all_groups = get_all_groups(session)
    random_group = random.choice(all_groups)
    return random_group.name


def select_random_subject(session):
    all_subjects = get_all_subjects(session)
    random_subject = random.choice(all_subjects)
    return random_subject.name


def select_1(session):
    """ Знайти 5 студентів з найбільшим середнім балом по всім предметам"""

    students = session.query(Student.name, cast(func.avg(Grade.value), Float)).\
        join(Student.grades).\
        group_by(Student).\
        order_by(func.avg(Grade.value).desc()).\
        limit(5).\
        all()
    return students


def select_2(session, subject_name):
    """Знайти студента із найвищим середнім балом з певного предмета."""

    student = session.query(Student.name, Subject.name, cast(func.avg(Grade.value), Float)).\
        join(Student.grades).\
        join(Grade.subject).\
        filter(Subject.name == subject_name).\
        group_by(Student, Subject).\
        order_by(func.avg(Grade.value).desc()).\
        first()
    return [student]


def select_3(session, subject_name):
    """Знайти середній бал у групах з певного предмета."""

    avg_grades = session.query(Group.name, Subject.name, cast(func.avg(Grade.value), Float)).\
        join(Group.students).\
        join(Student.grades).\
        join(Grade.subject).\
        group_by(Subject).\
        filter(Subject.name == subject_name).\
        group_by(Group).\
        all()
    return avg_grades


def select_4(session):
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""

    avg_grade = session.query(cast(func.avg(Grade.value), Float)).scalar()
    return avg_grade


def select_5(session, teacher_name):
    """Знайти які курси читає певний викладач."""

    courses = session.query(Teacher.name, Subject.name).\
        join(Subject.teacher).\
        filter(Teacher.name == teacher_name).\
        all()
    return courses


def select_6(session, group_name):
    """Знайти список студентів у певній групі."""

    students = session.query(Student.name).\
        join(Student.group).\
        filter(Group.name == group_name).\
        all()
    return students


def select_7(session, group_name, subject_name):
    """Знайти оцінки студентів у окремій групі з певного предмета."""

    grades = session.query(Group.name , Student.name, Subject.name, Grade.value).\
        join(Grade.student).\
        join(Grade.subject).\
        join(Student.group).\
        filter(Group.name == group_name, Subject.name == subject_name).\
        all()
    return grades



def select_8(session, teacher_name):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    avg_grade = session.query(cast(func.avg(Grade.value), Float)).\
        join(Subject, Subject.id == Grade.subject_id).\
        join(Teacher, Teacher.id == Subject.teacher_id).\
        filter(Teacher.name == teacher_name).\
        scalar()
    return avg_grade





def select_9(session, student_name):
    """Знайти список курсів, які відвідує певний студент."""

    courses = session.query(Student.name, Subject.name).\
        join(Subject.grades).\
        join(Grade.student).\
        filter(Student.name == student_name).\
        distinct().\
        all()
    return courses



def select_10(session, student_name, teacher_name):
    """Список курсів, які певному студенту читає певний викладач."""

    courses = session.query(Student.name, Subject.name, Teacher.name).\
        join(Subject.teacher).\
        join(Subject.grades).\
        join(Grade.student).\
        filter(Student.name == student_name, Teacher.name == teacher_name).\
        distinct().\
        all()
    return courses


def select_11(session, student_name, teacher_name):
    """Середній бал, який певний викладач ставить певному студентові."""

    avg_grade = session.query(cast(func.avg(Grade.value), Float)).\
        join(Grade.student).\
        join(Grade.subject).\
        join(Subject.teacher).\
        filter(Teacher.name == teacher_name).\
        filter(Student.name == student_name).\
        scalar()
    return avg_grade


def select_12(session, group_name, subject_name):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті."""

    grades = session.query(Subject.name, Group.name, Student.name, Grade.value).\
        join(Grade.student).\
        join(Grade.subject).\
        join(Subject.teacher).\
        join(Student.group).\
        filter(Group.name == group_name).\
        filter(Subject.name == subject_name).\
        order_by(Grade.created_at.desc()).\
        all()
    return grades




def execute_query(session, query_func, *args):

    # Виконання запиту
    result = query_func(session, *args)

    return result


if __name__ == '__main__':


    if check_connection():

        with DBSession() as session:

            queries = [
            (select_1,),
            (select_2, select_random_subject(session)),
            (select_3, select_random_subject(session)),
            (select_4,),
            (select_5, select_random_teacher(session)),
            (select_6, select_random_group(session)),
            (select_7, select_random_group(session), select_random_subject(session)),
            (select_8, select_random_teacher(session)),
            (select_9,  select_random_student(session)),
            (select_10, select_random_student(session), select_random_teacher(session)),
            (select_11, select_random_student(session), select_random_teacher(session)),
            (select_12, select_random_group(session), select_random_subject(session)),
        ]
                    
        # Виклик функції execute_query для кожного запиту
        for i, query in enumerate(queries):
            docstring = query[0].__doc__
            print(f"{i+1}: {docstring}\n")
            pprint(execute_query(session, *query))
            print("="*70)


