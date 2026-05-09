from datetime import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from extensions import db
from typing import Optional

# Objects representing entities in the database
class User(db.Model):
    __tablename__ = 'User'
    StudentID: so.Mapped[int] =so.mapped_column(primary_key=True)
    #Firstname: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    #Lastname: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    Username: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    Password: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    Course: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    Email: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    GraduationYear: so.Mapped[int] = so.mapped_column(nullable=False)
    Birthday: so.Mapped[datetime] = so.mapped_column(nullable=False)

class Faculty(db.Model):
    __tablename__ = 'Faculty'
    FacultyID: so.Mapped[int] = so.mapped_column(primary_key=True)
    Name: so.Mapped[str] = so.mapped_column(sa.String(20), nullable=False)

class GroupType(db.Model):
    __tablename__ = 'GroupType'
    GroupTypeID: so.Mapped[int] = so.mapped_column(primary_key=True)
    Type: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)

class Unit(db.Model):
    __tablename__ = 'Unit'
    UnitID: so.Mapped[int] = so.mapped_column(primary_key=True)
    UnitCode: so.Mapped[int] = so.mapped_column(nullable=False)
    UnitName: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    FacultyID: so.Mapped[int] = so.mapped_column(sa.ForeignKey('Faculty.FacultyID'), nullable=False)

class Groups(db.Model):
    __tablename__ = 'Groups'
    GroupID: so.Mapped[int] = so.mapped_column(primary_key=True)
    UnitID: so.Mapped[int] = so.mapped_column(sa.ForeignKey('Unit.UnitID'), nullable=False)
    GroupTypeID: so.Mapped[int] = so.mapped_column(sa.ForeignKey('GroupType.GroupTypeID'), nullable=False)
    Description: so.Mapped[str] = so.mapped_column(sa.String(200), nullable=False)
    CreationDate: so.Mapped[datetime] = so.mapped_column(nullable=False)
    GroupName: so.Mapped[str] = so.mapped_column(nullable=False)

class SessionType(db.Model):
    __tablename__ = 'SessionType'
    SessionTypeID: so.Mapped[int] = so.mapped_column(primary_key=True)
    Name: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)

class Role(db.Model):
    __tablename__ = 'Role'
    RoleID: so.Mapped[int] = so.mapped_column(primary_key=True)
    Type: so.Mapped[str] = so.mapped_column(sa.String(20), nullable=False)

class StudentGroups(db.Model):
    __tablename__ = 'StudentGroups'
    StudentID: so.Mapped[int] = so.mapped_column(sa.ForeignKey('User.StudentID'), primary_key=True)
    GroupID: so.Mapped[int] = so.mapped_column(sa.ForeignKey('Groups.GroupID'), primary_key=True)
    RoleID: so.Mapped[int] = so.mapped_column(sa.ForeignKey('Role.RoleID'), nullable=False)

class Session(db.Model):
    __tablename__ = 'Session'
    SessionID: so.Mapped[int] = so.mapped_column(primary_key=True)
    SessionDateTime: so.Mapped[datetime] = so.mapped_column(nullable=False)
    Description: so.Mapped[str] = so.mapped_column(sa.String(200), nullable=False)
    GroupID: so.Mapped[int] = so.mapped_column(sa.ForeignKey('Groups.GroupID'), nullable=False)
    SessionTypeID: so.Mapped[int] = so.mapped_column(sa.ForeignKey('SessionType.SessionTypeID'), nullable=False)
    Location: so.Mapped[str] = so.mapped_column(nullable=False)