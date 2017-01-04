from app import db


class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String)


class Stories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_title = db.Column(db.String)
    description = db.Column(db.String)
    containing_epic = db.Column(db.Integer, db.ForeignKey('epics.id'))
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'))


class Epics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))


class RoleStories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))


class Steps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    type = db.Column(db.Integer)
    content = db.Column(db.String)
    step_num = db.Column(db.Integer)


class Assumptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    assumption = db.Column(db.String)
    containing_id = db.Column(db.Integer, db.ForeignKey('stories.id'))


class Workflows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String)

