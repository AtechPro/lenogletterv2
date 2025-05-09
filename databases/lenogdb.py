import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import bcrypt

Base = declarative_base()

class LetterForm(Base):
    __tablename__ = 'letters'

    id = Column(Integer, primary_key=True)
    letter_type = Column(String(10))
    reference_no = Column(String(100))
    contract_title = Column(String(200))
    subject = Column(String(300))
    contact_name = Column(String(100))
    designation = Column(String(100))
    no = Column(String(50))           
    email = Column(String(100))       
    documents = Column(Text)

    def set_documents(self, doc_list):
        self.documents = json.dumps(doc_list)

    def get_documents(self):
        return json.loads(self.documents or "[]")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    def set_password(self, password):
        """Hashes and stores the password."""
      
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password):
        """Verifies the password against the stored hash."""
        
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))


# === PATH CONFIGURATION ===

# Ensure the ./databases folder exists
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = os.path.join(BASE_DIR)
os.makedirs(DB_FOLDER, exist_ok=True)

# Local (default for now)
LOCAL_DB_PATH = os.path.join(DB_FOLDER, 'letterdata.db')

# Backup (future Z drive)
Z_DRIVE_DB_PATH = r'Z:\Technical\02 Research & Development\Letter GUI\letterdata.db'

# Switch here (use LOCAL for now)
db_path = LOCAL_DB_PATH
# db_path = Z_DRIVE_DB_PATH

engine = create_engine(f'sqlite:///{db_path}')
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
