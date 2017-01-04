from app import db


class Roles(db.Model):
    id = db.column(db.Integer, primary_key=True)
    role_name = db.column(db.String)


class Stories(db.model):
    id = db.column(db.Integer, primary_key=True)
    story_title = db.column(db.String)
    description = db.column(db.String)
    containing_epic = db.column(db.Integer, db.ForeignKey('stories.id'))
    contained_stories = db.relationship('Stories', backref='inside_stories', lazy='dynamic')


