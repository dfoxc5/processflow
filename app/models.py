from app import db, app


class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String)


class Stories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_title = db.Column(db.String)
    description = db.Column(db.String)
    containing_epic = db.Column(db.Integer, db.ForeignKey('epics.epic_id'))
    contained_stories = db.relationship('Epics', backref='inside_stories', lazy='dynamic')


class Epics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    epic_id = db.Column(db.Integer)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))


