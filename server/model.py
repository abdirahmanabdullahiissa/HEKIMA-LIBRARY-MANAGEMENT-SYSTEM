from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import SQLAlchemy,db,bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

class User(db.Model, SerializerMixin):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False)
    _password_hash=db.Column(db.String,nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

    roles=db.relationship("Role", secondary="user_roles", back_populates="users")

    def has_role(self, role):
        return (
            Role.query
            .join(UserRole)
            .filter(UserRole.user_id == self.id)
            .filter(Role.slug == role)
            .count() == 1

        )

    def serialize(self):
        return {"id":self.id,"username":self.username,"email":self.email,"created_at":self.created_at}



class Role(db.Model,SerializerMixin):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    slug=db.Column(db.String,nullable=False, unique=True)

    users=db.relationship("User", secondary="user_roles", back_populates="roles")

    def serialize(self):
        return {"id":self.id,"name":self.name,"slug":self.slug}


class UserRole(db.Model,SerializerMixin):
    __tablename__="user_roles"
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),primary_key=True)
    role_id=db.Column(db.Integer, db.ForeignKey("roles.id"),primary_key=True)

class Book(db.Model,SerializerMixin):
    __tablename__="books"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    author=db.Column(db.String,nullable=False)
    isbn=db.Column(db.String(13),unique=True, nullable=False)
    publication_year=db.Column(db.Integer, nullable=True)
    copies_available=db.Column(db.Integer,default=1, nullable=False)

    def serialize(self):
        return {"id":self.id,"name":self.name,"author":self.author,"publication_year":self.publication_year,"copies_available":self.copies_available}


class BorrowedBook(db.Model):
    __tablename__ = "borrowed_books"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrowed_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    returned_at = db.Column(db.DateTime, nullable=True)
    user = db.relationship('User', backref='borrowed_books')
    book = db.relationship('Book', backref='borrowed_books')

    def serialize(self):
        return {"id":self.id,"borrowed_at":self.borrowed_at,"due_date":self.due_date,"returned_at":self.returned_at}