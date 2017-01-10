from app import db, models
from sqlalchemy.engine import reflection
from sqlalchemy.schema import (
        MetaData,
        Table,
        DropTable,
        ForeignKeyConstraint,
        DropConstraint,
        )


def init_database():
    # drop_everything(db)
    db.create_all()
    roles = models.Roles.query.all()
    if len(roles) is 0:
        create_roles()
    # stories = models.Stories.query.all()
    # if len(stories) is 0:
    #     create_test_stories()


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
    new_story = models.Stories(story_title="Test 1", description="Test", containing_epic=None, workflow_id=None)
    db.session.add(new_story)
    new_story = models.Stories(story_title="Test 2", description="Test", containing_epic=None, workflow_id=None)
    db.session.add(new_story)
    db.session.commit()


def drop_everything(db):
    # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything

    conn = db.engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(db.engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in
    # a transaction.
    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((), (), name=fk['name'])
            )
        t = Table(table_name, metadata, *fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()
