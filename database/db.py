"""
Код для встановлення та налаштування з'єднання з базою даних. Забезпечує зв'язок між додатком і базою даних, даючи змогу
додатку взаємодіяти з даними, що зберігаються в цій базі .""" 

import configparser
from pathlib import Path
from sqlalchemy.exc import OperationalError


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#  postgresql://username:password@host:port/database_name
file_config = Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

user_name = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
database_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')
port= config.get('DB', 'PORT')
url = f'postgresql://{user_name}:{password}@{domain}:{port}/{database_name}'

def check_connection():
    try:
        engine = create_engine(url, echo=False)
        connect = engine.connect()
        connect.close()
        print("The connection to the database is established.")
        return True
    except OperationalError:
        print("Failed to connect to the database.")
        return False

engine = create_engine(url, echo=False)
DBSession = sessionmaker(bind=engine)

