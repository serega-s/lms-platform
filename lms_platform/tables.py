import sqlalchemy as sa

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    email = sa.Column(sa.String(150), nullable=False, unique=True)
    password = sa.Column(sa.String, nullable=False)
    role = sa.Column(sa.String(10))
    created_at = sa.Column(sa.TIMESTAMP(timezone=True),
                           nullable=False, server_default=sa.text('now()'))


class Course(Base):
    __tablename__ = 'courses'

    id = sa.Column(sa.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    title = sa.Column(sa.String(255))
    slug = sa.Column(sa.String)
    short_description = sa.Column(sa.String(500))
    description = sa.Column(sa.dialects.postgresql.TEXT)
    image = sa.Column(sa.String)
    lessons = sa.orm.relationship(
        'Lesson', backref='Lesson.id')  # lazy='dynamic'
    created_at = sa.Column(sa.TIMESTAMP(timezone=True),
                           nullable=False, server_default=sa.text('now()'))


class Lesson(Base):
    __tablename__ = 'lessons'

    id = sa.Column(sa.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    course_id = sa.Column(sa.Integer, sa.ForeignKey(
        "courses.id", ondelete="CASCADE"), nullable=False)
    title = sa.Column(sa.String(255))
    slug = sa.Column(sa.String)
    short_description = sa.Column(sa.String(500))
    description = sa.Column(sa.dialects.postgresql.TEXT)
    draft = sa.Column(sa.Boolean, default=True)
    created_at = sa.Column(sa.TIMESTAMP(timezone=True),
                           nullable=False, server_default=sa.text('now()'))


class Profile(Base):
    __tablename__ = 'profiles'

    id = sa.Column(sa.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False, unique=True)
    user = sa.orm.relationship("User")
    full_name = sa.Column(sa.String(150))
    bio = sa.Column(sa.String(3000))
    phone_number = sa.Column(sa.String(100))
    image = sa.Column(sa.String)
    created_at = sa.Column(sa.TIMESTAMP(timezone=True),
                           nullable=False, server_default=sa.text('now()'))


class Comment(Base):
    __tablename__ = 'comments'

    id = sa.Column(sa.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    content = sa.Column(sa.String(400))
    course_id = sa.Column(sa.Integer, sa.ForeignKey(
        "courses.id", ondelete="CASCADE"), nullable=False)
    lessons_id = sa.Column(sa.Integer, sa.ForeignKey(
        "lessons.id", ondelete="CASCADE"), nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey( 
        "users.id", ondelete="CASCADE"), nullable=False)
    created_at = sa.Column(sa.TIMESTAMP(timezone=True),
                           nullable=False, server_default=sa.text('now()'))
