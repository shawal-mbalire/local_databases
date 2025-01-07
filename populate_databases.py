from faker import Faker
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
import random
import os

fake = Faker()

def construct_db_uri(db_type):
    user        = os.getenv(f'{db_type.upper()}_USER', 'admin')
    password    = os.getenv(f'{db_type.upper()}_PASSWORD', 'superadmin')
    host        = os.getenv(f'{db_type.upper()}_HOST', 'localhost')
    port        = os.getenv(f'{db_type.upper()}_PORT', '5432')
    database    = os.getenv(f'{db_type.upper()}_DATABASE', 'our_db')

    return f"{db_type}://{user}:{password}@{host}:{port}/{database}"

DATABASES = {
    'postgres': construct_db_uri('postgresql'),
    # 'mysql': construct_db_uri('mysql+pymysql'),
    # 'mariadb': construct_db_uri('mysql+pymysql'),
    # 'oracle': construct_db_uri('oracle+cx_oracle')
}

Base = declarative_base()

# Define ORM class
class Person(Base):
    __tablename__ = 'persons'

    id                      = Column(Integer, primary_key=True) #0
    full_name               = Column(String(100)) #1
    date_of_birth           = Column(String(20))  #2
    email                   = Column(String(100)) #3
    gender                  = Column(String(10))  #4
    national_id             = Column(String(20))  #5
    phone_number            = Column(String(20))  #6
    passport_number         = Column(String(20))  #7
    age                     = Column(Integer)     #8
    city                    = Column(String(50))  #9
    country                 = Column(String(50))  #10
    state                   = Column(String(50))  #11
    zip_code                = Column(String(20))  #12
    occupation              = Column(String(50))  #13
    marital_status          = Column(String(20))  #14
    education_level         = Column(String(50))  #15
    hobbies                 = Column(String(200)) #16
    language_preferences    = Column(String(200)) #17
    status                  = Column(String(20))  #18

# Helper function to truncate text
def truncate(text, length):
    return text[:length]

# Generate fake data
def generate_fake_data():
    return Person(
        age=                    random.randint(18, 80),
        date_of_birth=          fake.date_of_birth().strftime('%Y-%m-%d'),
        full_name=              truncate(fake.name(), 100),
        email=                  truncate(fake.email(), 100),
        gender=                 truncate(random.choice(['Male', 'Female', 'Other']), 10),
        national_id=            truncate(fake.ssn(), 20),
        phone_number=           truncate(fake.phone_number(), 20),
        passport_number=        truncate(fake.pystr(min_chars=8, max_chars=12), 20),
        city=                   truncate(fake.city(), 50),
        country=                truncate(fake.country(), 50),
        state=                  truncate(fake.state(), 50),
        zip_code=               truncate(fake.zipcode(), 20),
        occupation=             truncate(fake.job(), 50),
        marital_status=         truncate(random.choice(['Single', 'Married', 'Divorced']), 20),
        education_level=        truncate(random.choice(['High School', 'Bachelor', 'Master', 'PhD']), 50),
        hobbies=                truncate(', '.join(fake.words(nb=5)), 200),
        language_preferences=   truncate(', '.join(fake.words(nb=3)), 200),
        status=                 "UNHASHED"
    )

# Populate data into the database
def populate_data(session):
    for _ in range(100):  # Insert 100 records
        person = generate_fake_data()
        session.add(person)
    session.commit()

if __name__ == "__main__":
    for db, uri in DATABASES.items():
        engine = create_engine(uri)
        Session = sessionmaker(bind=engine)
        session = Session()

        Base.metadata.drop_all(engine)  # Ensure table is dropped before creation
        Base.metadata.create_all(engine)

        print(f"Populating {db} database...")
        populate_data(session)
        print(f"Populated {db} database with fake data.")
