"""Цей код являє собою сценарій для генерації випадкових даних про студентів,
вчителів та оцінки, а також їх додавання в базу даних. Групи та предмети
генеруються не випадково, а задаються в коді у вигляді списків.
"""

import random
import logging

from faker import Faker
from database.db import DBSession, check_connection

from database.repository import create_student,\
                                create_group,\
                                create_teacher,\
                                create_subject,\
                                create_grade,\
                                clear_database

from database.db import engine
from database.models import Base




if check_connection():

    # Створюємо базу данних
    Base.metadata.create_all(engine)

    #Створюємо сесію
    session = DBSession()

    fake = Faker("uk_UA")

    # Конфігурація логування
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


    # Конфігурація логування
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Створюємо логгер
    logger = logging.getLogger(__name__)

    # Створюємо обробник для виведення попереджень у консоль
    warning_handler = logging.StreamHandler()
    warning_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    warning_handler.setFormatter(formatter)

    # Додаємо обробник до логгера
    logger.addHandler(warning_handler)

    # Очищуємо базу даних перед внесенням даних
    clear_database(session=session)


    # Створюємо 5 вчителів
    teachers = []
    for _ in range(5):
        teacher = create_teacher(session=session, name=fake.name())
        teachers.append(teacher)

    # Створюємо предмети з відповідними вчителями
    subjects = []
    subject_names = ["Фізика", "Математика", "Філософія", "Історія", "Українська мова"]
    for subject_name, teacher in zip(subject_names, teachers):
        subject = create_subject(session=session, name=subject_name, teacher=teacher)
        subjects.append(subject)

    # Створюємо 3 групи
    groups = []
    group_names = ["АСУ-11", "АСУ-12", "АСУ-13"]
    for group_name in group_names:
        group = create_group(session=session, name=group_name)
        groups.append(group)

    # Створюємо 40 студентів
    for _ in range(40):
        student_name = fake.name()
        group = random.choice(groups)
        student = create_student(session=session, name=student_name, group_id=group.id)

        # Створюємо 20 оцінок для кожного студента з усіх предметів
        for _ in range(20):
            subject = random.choice(subjects)
            value = fake.random_int(min=1, max=100)
            create_grade(session=session, student=student, subject=subject, value=value)

    logger.info("Data was successfully generated and added to the database.")

    session.close()