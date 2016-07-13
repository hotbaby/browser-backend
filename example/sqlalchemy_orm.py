
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

"""
Connect DB.
"""
engine = create_engine("mysql://test:test@192.168.1.204/test", echo=True)

"""
Declare a Mapping
"""
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    fullname = Column(String(20))
    password = Column(String(20))
    
#     addresses = relationship("Address", back_populates="users")
    
    def __repr__(self):
        return "<User(name=%s, fullname=%s, password=%s)>" \
            % (self.name, self.fullname, self.password)


"""
Building a Relationship
"""

# class Address(Base):
#     __tablename__ = "addresses"
#     id = Column(Integer, primary_key=True)
#     email_address = Column(String(64), nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"))
#       
#     user = relationship("User", back_populates="addresses")
#       
#     def __repr__(self):
#         return "<Address(email_address='%s')>" % self.email_address


# Textual SQL
# CREATE TABLE addresses (
#     id INTEGER NOT NULL AUTO_INCREMENT, 
#     email_address VARCHAR(64) NOT NULL, 
#     user_id INTEGER, 
#     PRIMARY KEY (id), 
#     FOREIGN KEY(user_id) REFERENCES users (id)
# )
    
Base.metadata.create_all(engine)    
"""
Create the schema.
The MetaData is a registry which includes the ability to emit a limited of schema generation commands to the database.
As our SQLite database does not actually have a 'users' table present, we can use MetaData to issue 'CREATE TABLE' 
statements to the database for all tables that don't yet exist. Below, we call the 'MetaData.create_all()' method,
passing in our 'Engine' as a source of database connectivity.
"""
# Base.metadata.create_all(engine)


"""
Create an instance of the Mapped Class
"""
ed = User(name="ed", fullname="Ed Jones", password="edpassword")

"""
Create a Session
We're now ready to start talking to the database. The ORM's 'handle' to the database is the 'session'. When we first 
setup the application, at the same level as our 'create_engine()' statement, we define a 'Session' class which will
serve as a factory for new 'Session' objects.

This custome-made Session class will create new Session object which are bound to our database. The below Session is
associated with our myql engine, but it hasn't opened any connections yet.When it's first used, it retrieves a connection
from a pool of connections maintained by the Egine, and holds onto it until we commit all changes and/or close session
object.
"""
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# Session = sessionmaker()
# Session.configure(bind=engine)

"""
Adding and Updating Objects.
To persist out User object, we add() ti to out Session.
"""
session.add(ed)
# session.commit()

"""
Rolling Back
Since the Session works within a transaction, we can roll back changes made too.
"""
fake_user = User(name="fakeuser", fullname="invalid", password="fakeuser")
session.add(fake_user)
print(session.query(User).all())
# session.rollback()
print(session.query(User).all())

"""
Querying
"""
for ins in session.query(User).order_by(User.id):
    print(ins.name, ins.fullname)
    
for name, fullname in session.query(User.name, User.fullname).all():
    print(name, fullname)
    
for row in session.query(User, User.name).all():
    print(row.User, row.name)
    
"""
You can control the names of individual column expressions using the label() construct, which is availbale from any 
ColumnElement derived object, as well as any class attribute which is mapped to one 
"""
for row in session.query(User.name.label("name_label")).all():
    print(row.name_label)

"""
The name given to a full entity such as User, assuming that multiple entities are present in the call to query(), can
be controlled using aliased()
"""
from sqlalchemy.orm import aliased
user_alias = aliased(User)
for row in session.query(user_alias).all():
    print(row)
    
for user in session.query(User).filter_by(fullname="Ed Jones").all():
    print(user)
    
for user in session.query(User).order_by(User.id)[0:1]:
    print(user)

for user in session.query(User).\
            filter_by(name="ed").\
            filter_by(fullname="Ed Jones").\
            filter_by(id=0):
    print(user)

"""
Common Filter Operators
"""
#equals
session.query(User).filter(User.name=="ed")
#not equal
session.query(User).filter(User.name!="ed")
#LIKE
session.query(User).filter(User.name.like("%ed%"))
#IN
session.query(User).filter(User.name.in_(["ed", "jack"]))
session.query(User).filter(User.name.in_(session.query(User).filter(User.name.like("%ed%"))))
#Not IN
for user in session.query(User).filter(~User.name.in_(["ed"])):
    print(user)
#IS NULL
session.query(User).filter(User.name==None)
session.query(User).filter(User.name.is_(None))

#IS NOT NULL
session.query(User).filter(User.name != None)
session.query(User).filter(User.name.isnot(None))

#AND
from sqlalchemy import and_
session.query(User).filter(and_(User.name == "ed", User.fullname == "Ed Jones"))
session.query(User).filter(User.name == "ed").filter(User.fullname == "Ed Jones")

#OR 
from sqlalchemy import or_
session.query(User).filter(or_(User.name == "ed", User.fullname == "Ed Jones"))

#MATCH
session.query(User).filter(User.name.match("ed"))

"""
Returning Lists and Scalars
"""
query = session.query(User).filter(User.name=="ed").order_by(User.id)
query.all()
query.first()

"""
Using Textual SQL
"""
from sqlalchemy import text
stmt = text("SELECT name, id FROM users where name=:name")
session.query(User).from_statement(stmt).params(name="ed").all()

"""
Counting
"""
from sqlalchemy import func
session.query(User).filter(User.name.like("ed")).count()
session.query(func.count(User.name), User.name).group_by(User.name).all() 
#Textual SQL, SELECT count(users.name) AS count_1, users.name AS users_name FROM users GROUP BY users.name
session.query(func.count("*")).select_from(User).scalar()
#Textual SQl,  SELECT count(%s) AS count_1 FROM users
session.query(func.count(User.id)).scalar()


"""
Working with Related Objects
"""
jack = User(name="jack", fullname="Jack Bean", password="jack@")
# jack.addresses = [Address(email_address="jack@google.com")]
session.add(jack)
session.commit()
