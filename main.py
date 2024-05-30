"""Код  взаємодії з базою даних студентів із командного рядка,
виконуючи різні операції з об'єктами моделей: створення, оновлення,
видалення, отримання інформації та виведення списку."""


import logging
from argparse import ArgumentParser
import database.repository as dr
from database.db import DBSession, check_connection



# Creating a command line argument parser
parser = ArgumentParser(description='Students DB')
parser.add_argument('--action', '-a', help='Commands: create, get, update, remove, list')
parser.add_argument('--model', '-m', help='Models: Teacher, Group, Student, Subject, Grade')
parser.add_argument('--id', help='ID of the object')
parser.add_argument('--name', '-n', help='Name of the object')
parser.add_argument('--subject', '-s', help='Subject of the object')
parser.add_argument('--group', '-g', help='Group of the student')
parser.add_argument('--value', '-v', help='Value of the object')

# Parsing command line arguments
arguments = parser.parse_args()
my_args = vars(arguments)

action = my_args.get('action')
model = my_args.get('model')
id = my_args.get('id')
name = my_args.get('name')
subject = my_args.get('subject')
value = my_args.get('value')
group = my_args.get('group')

#  Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


#  Defining functions for CRUD operations

def create(session):
    try:
        if not name:
            raise ValueError('Name parameter is missing')

        match model:
            case 'Teacher': 
                dr.create_teacher(session, name)
                logging.info('Teacher created: %s', name)
            case 'Group': 
                dr.create_group(session, name)
                logging.info('Group created: %s', name)
            case 'Student':
                dr.create_student(session, name, group)
                logging.info('Student created: %s', name)
            case 'Subject':
                teacher = dr.get_teacher(session, id)
                dr.create_subject(session, name, teacher)
                logging.info('Subject created: %s', name)
            case 'Grade':
                student = dr.get_student(session, id)
                subject = dr.get_subject(session, subject)
                dr.create_grade(session, student, subject, value)
                logging.info('Grade created for student ID %s and subject ID %s', id, subject)
    except ValueError as ve:
        logging.error('ValueError: %s', str(ve))
    except Exception as e:
        logging.error('Error occurred during create operation: %s', str(e))

def update(session):
    try:
        if not model:
            raise ValueError('Model parameter is missing')
        
        if not id:
            raise ValueError('ID parameter is missing')
        
        match model:
            case 'Teacher':
                dr.update_teacher(session, id, name)
                logging.info('Teacher updated: ID %s, new name: %s', id, name)
            case 'Group':
                dr.update_group(session, id, name)
                logging.info('Group updated: ID %s, new name: %s', id, name)
            case 'Student':
                dr.update_student(session, id, name)
                logging.info('Student updated: ID %s, new name: %s', id, name)
            case 'Subject':
                dr.update_subject(session, id, name)
                logging.info('Subject updated: ID %s, new name: %s', id, name)
            case 'Grade':
                dr.update_grade(session, id, value)
                logging.info('Grade updated: ID %s, new value: %s', id, value)

    except ValueError as ve:
        logging.error('ValueError: %s', str(ve))
    except Exception as e:
        logging.error('Error occurred during update operation: %s', str(e))

def remove(session):
    try:

        if not id:
            raise ValueError('ID parameter is missing')
        
        match model:
            case 'Teacher':
                dr.delete_teacher(session, id)
                logging.info('Teacher deleted: ID %s', id)
            case 'Group':
                dr.delete_group(session, id)
                logging.info('Group deleted: ID %s', id)
            case 'Student':
                dr.delete_student(session, id)
                logging.info('Student deleted: ID %s', id)
            case 'Subject':
                dr.delete_subject(session, id)
                logging.info('Subject deleted: ID %s', id)
            case 'Grade':
                dr.delete_grade(session, id)
                logging.info('Grade deleted: ID %s', id)

    except ValueError as ve:
        logging.error('ValueError: %s', str(ve))
    except Exception as e:
        logging.error('Error occurred during remove operation: %s', str(e))

def get(session):
    try:

        if not id:
            raise ValueError('ID parameter is missing')

        match model:
            case 'Teacher':
                teacher = dr.gteacher(session, id)
                logging.info('Teacher details: ID %s, Name: %s', id, teacher.name)
            case 'Group':
                group = dr.ggroup(session, id)
                logging.info('Group details: ID %s, Name: %s', id, group.name)
            case 'Student':
                student = dr.gstudent(session, id)
                logging.info('Student details: ID %s, Name: %s', id, student.name)
            case 'Subject':
                subject = dr.gsubject(session, id)
                logging.info('Subject details: ID %s, Name: %s', id, subject.name)
            case 'Grade':
                grade = dr.ggrade(session, id)
                logging.info('Grade details: ID %s, Value: %s', id, grade.value)

    except ValueError as ve:
        logging.error('ValueError: %s', str(ve))
    except Exception as e:
        logging.error('Error occurred during get operation: %s', str(e))

def list_(session):
    try:

        match model:
            case 'Teacher':
                dr.list_teachers(session)
            case 'Group':
                dr.list_groups(session)
            case 'Student':
                dr.list_students(session)
            case 'Subject':
                dr.list_subjects(session)
            case 'Grade':
                dr.list_grades(session)

    except Exception as e:
        logging.error('Error occurred during get operation: %s', str(e))


if __name__ == "__main__":


    if check_connection():
        # Виклик відповідної функції залежно від команди

        with DBSession() as session:
            match action:
                case 'create':
                    create(session)
                case 'update':
                    update(session)
                case 'remove':
                    remove(session)
                case 'get':
                    get(session)
                case 'list':
                    list_(session)
                case _:
                    parser.print_help()
