from app import db, models


def init_database():
    # db.drop_all()
    db.create_all()
    roles = models.Roles.query.all()
    if len(roles) is 0:
        create_roles()
    stories = models.Stories.query.all()
    if len(stories) is 0:
        create_test_stories()


def create_roles():
    new_role1 = models.Roles(role_name="Staff Member")
    new_role2 = models.Roles(role_name="PO")
    new_role3 = models.Roles(role_name="Other")
    new_role4 = models.Roles(role_name="Index")
    db.session.add(new_role1)
    db.session.add(new_role2)
    db.session.add(new_role3)
    db.session.add(new_role4)
    db.session.commit()


def create_test_stories():
    new_story = models.Stories(story_title="Test 1", description="Test", containing_epic=0, workflow_id=1)
    db.session.add(new_story)
    db.session.commit()
