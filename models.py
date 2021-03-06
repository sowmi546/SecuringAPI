from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
from passlib.hash import sha256_crypt
from sqlalchemy.schema import Sequence
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, Sequence('user_id_seq', start=1001, increment=1), primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = sha256_crypt.encrypt(password)
        print (isinstance(self.password_hash, (str)))
        print("Hello %s", self.password_hash)



    def verify_password(self, password):
        return sha256_crypt.verify(password, self.password_hash)
        # return pwd_context.verify(password, self.password_hash)


engine = create_engine('sqlite:///users.db')


Base.metadata.create_all(engine)
