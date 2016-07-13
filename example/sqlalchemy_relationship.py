
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.selectable import subquery
from sqlalchemy.orm.util import outerjoin


engine = create_engine("mysql://test:test@192.168.1.204/test", echo=True)
Base = declarative_base(engine)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    fullname = Column(String(32))
    
    def __repr__(self):
        return "<User(name=%s, fullname=%s)>" % (self.name, self.fullname)


class Address(Base):
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True)
    email_address = Column(String(32), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", backref="addresses")
    
    def __repr__(self):
        return "<Address(email_address=%s)>" % self.email_address


from sqlalchemy import Table
post_keywords = Table("post_keywords", Base.metadata,
                      Column("post_id", ForeignKey("posts.id", primary_key=True)),
                      Column("keyword_id", ForeignKey("keywords.id", primary_key=True)))

class BlogPost(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    headline = Column(String(255), nullable=False)
    body = Column(Text)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="posts")
    
    keywords = relationship("Keyword",
                            secondary=post_keywords)
    

class Keyword(Base):
    __tablename__ = "keywords"
    
    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)
    posts = relationship("BlogPost",
                         secondary=post_keywords)
    
    def __repr__(self):
        return "Keyword(keyword=%s)" % self.keyword
    
    
Base.metadata.drop_all()

Base.metadata.create_all()

Session = sessionmaker(bind=engine)
session = Session()
  

"""
Working with Related Objects
"""
jack = User(name="jack", fullname="Jack Jones")
jack.addresses=[
                Address(email_address="jack@google.com"),
                Address(email_address="jack@facebook.com")]
session.add(jack)
session.commit()

"""
Querying with Joins
"""
for user, addr in session.query(User, Address).\
                  filter(User.id == Address.user_id).\
                  filter(Address.email_address == "jack@google.com").\
                  all():
    print(user, addr)
for user in session.query(User).join(Address).\
            filter(Address.email_address == "jack@google.com").\
            all():
    print(user, user.addresses)

"""
Using aliases
"""
from sqlalchemy.orm import aliased
addr_alias1 = aliased(Address)
addr_alias2 = aliased(Address)
for name, addr1, addr2 in session.query(User.name, addr_alias1.email_address, addr_alias2.email_address).\
                          join(addr_alias1).\
                          join(addr_alias2).\
                          filter(addr_alias1.email_address == "jack@google.com").\
                          filter(addr_alias2.email_address == "jack@facebook.com"):
    print(name, addr1, addr2)
    
"""
Using Subqueries
"""
from sqlalchemy.sql import func
stmt = session.query(Address.user_id, func.count("*").label("address_count")).\
       group_by(Address.user_id).\
       subquery()
       
"""
Once we have our statement, it behaves like a Table construct, such as the one we created for 'users' at the
start of this tutorial. The columns on the statement are accessible through an attribute called c:
"""
for user, count in session.query(User, stmt.c.address_count).\
                   outerjoin(stmt, User.id == stmt.c.user_id).\
                   order_by(User.id):
    print(user, count)

# Textual SQl
# SELECT users.id AS users_id, users.name AS users_name, users.fullname AS users_fullname, anon_1.address_count AS anon_1_address_count 
# FROM users LEFT OUTER JOIN (SELECT addresses.user_id AS user_id, count(%s) AS address_count 
# FROM addresses GROUP BY addresses.user_id) AS anon_1 ON users.id = anon_1.user_id ORDER BY users.id

"""
Using EXISTS
"""
from sqlalchemy.sql import exists
stmt = exists().where(Address.user_id == User.id)
for name in session.query(User.name).filter(stmt):
    print(name)

"""
Common Relationship Operators
"""

"""
Deleting
"""
# session.delete(jack)
# session.commit()

"""
Build Many To Many Relationship
"""