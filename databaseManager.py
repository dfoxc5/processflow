import sqlite3
import psycopg2


class DatabaseManager:
    role = 0
    approved_files = ['.gif', '.GIF']

    def __init__(self):
        pass

    def set_role(self, role_num):
        self.role = role_num

    def get_role_name(self, data):
        mysql = "SELECT ROLES.role_name FROM ROLES WHERE role_id=" + str(self.role)
        data.execute(mysql)
        role_name = data.fetchone()[0]
        return role_name

    @staticmethod
    def get_roles():
        db = psycopg2.connect("host='127.0.0.1' dbname='postgres' user='postgres' password='password'")
        # db = sqlite3.connect('testDB.db')
        data = db.cursor()
        data.execute('SELECT * FROM ROLES')
        roles = data.fetchall()
        return roles

    @staticmethod
    def get_all_stories():
        db = psycopg2.connect("host='127.0.0.1' dbname='postgres' user='postgres' password='password'")
        data = db.cursor()
        data.execute('SELECT story_title FROM USER_STORIES')
        temp = data.fetchall()
        stories = []
        for story in temp:
            stories.append(story[0])
        return stories

    @staticmethod
    def get_all_epics():
        db = psycopg2.connect("host='127.0.0.1' dbname='postgres' user='postgres' password='password'")
        data = db.cursor()
        data.execute('SELECT * FROM USER_STORIES')
        temp = data.fetchall()
        epics = []
        for story_id in temp:
            mysql = "SELECT * FROM STEPS WHERE story_id='" + str(story_id[0]) + "'"
            data.execute(mysql)
            check = data.fetchone()
            if check is None:
                epics.append(story_id[1])
        return epics

    def get_stories(self, epic):
        db = psycopg2.connect("host='127.0.0.1' dbname='postgres' user='postgres' password='password'")
        data = db.cursor()
        story_list = []
        if epic == '0':
            role = self.role
            if role is not 0:
                if role == '4':
                    data.execute("SELECT * FROM USER_STORIES WHERE containing_epic IS NULL")
                    stories = data.fetchall()
                    return stories
                my_sql = "SELECT ROLE_STORIES.story_id FROM ROLE_STORIES WHERE ROLE_STORIES.role_id=" + role
                data.execute(my_sql)
                stories = data.fetchall()
                story_list = []
                for story in stories:
                    mysql = "SELECT * FROM USER_STORIES WHERE story_id =" + str(story[0]) + " AND containing_epic IS NULL"
                    data.execute(mysql)
                    story = []
                    temp = data.fetchone()
                    if temp:
                        for element in temp:
                            story.append(element)
                        # if 'user' in story[2]:
                        #     role_name = self.get_role_name(data)
                        #     story[2] = str(story[2]).replace("user", role_name).lower()
                        story_list.append(story)
        else:
            mysql = "SELECT * FROM USER_STORIES WHERE containing_epic=" + str(epic)
            data.execute(mysql)
            temp = data.fetchall()
            story_list = []
            if temp:
                for story in temp:
                    story_list.append(story)
        return story_list

    @staticmethod
    def get_epic(epic_title, data):
        epic_title = str(epic_title)
        my_sql = "SELECT USER_STORIES.story_id FROM USER_STORIES WHERE USER_STORIES.story_title='" + epic_title + "'"
        data.execute(my_sql)
        epic_id = str(data.fetchone())
        if epic_id != 'None':
            return epic_id[1]
        else:
            return 0

    @staticmethod
    def create_user_story(name, description, workflow, epic_title, data):
        name = str(name)
        description = str(description)
        if epic_title == 0:
            epic_title = None
        else:
            epic_title = str(epic_title)
        if workflow == '':
            workflow = None
        else:
            workflow = str(workflow)
        userstory_id = 0
        if name != '':
            if description != '':
                try:
                    data.execute('INSERT INTO USER_STORIES (story_title, description, containing_epic, workflow_id) VALUES (%s, %s, %s, %s) RETURNING story_id', (name, description, epic_title, workflow))
                    userstory_id = data.fetchone()[0]
                except sqlite3.IntegrityError:
                    return "This story already exists"
        return userstory_id

    @staticmethod
    def create_assumptions(story_id, assumptions, links, data):
        story_id = str(story_id)
        if assumptions:
            for i, assumption in enumerate(assumptions):
                assumption = str(assumption)
                if len(links[i]) > 1:
                    mysql = "SELECT story_id FROM USER_STORIES WHERE story_title='" + links[i] + "'"
                    data.execute(mysql)
                    link = data.fetchone()[0]
                else:
                    link = 0
                data.execute("INSERT INTO ASSUMPTIONS (story_id, assumption, containing_story) VALUES (%s, %s, %s)", (story_id, assumption, link))

    def create_steps(self, story_id, story_title, steps, data):
        story_id = str(story_id)
        step_num = 1
        if steps:
            for step in steps:
                step = str(step)
                if any(x in step for x in self.approved_files):
                    if "static%2Fimages%2Fuploads%2F" not in step:
                        step = "static/images/uploads/" + str(story_title).replace(" ", "_").lower() + "_" + step
                    step_type = 3
                elif step[0] == "(":
                    step_type = 2
                else:
                    step_type = 1
                data.execute('INSERT INTO STEPS (story_id, type, content, step_num) VALUES (%s, %s, %s, %s)', (story_id, step_type, step, step_num))
                step_num += 1

    @staticmethod
    def create_role_story(roles, story_id, data):
        story_id = str(story_id)
        role_num = 1
        for role in roles:
            if role == 'checked':
                role_id = role_num
                data.execute("INSERT INTO ROLE_STORIES (role_id, story_id) VALUES (%s, %s)", (role_id, story_id))
            role_num += 1

    def save_story(self, roles, epic_title, title, description, assumptions, linked_stories, workflow, steps):
        db = psycopg2.connect("host='127.0.0.1' dbname='postgres' user='postgres' password='password'")
        data = db.cursor()
        epic_title = self.get_epic(epic_title, data)
        story_id = self.create_user_story(title, description, workflow, epic_title, data)
        if story_id != 0:
            self.create_role_story(roles, story_id, data)
            if assumptions:
                self.create_assumptions(story_id, assumptions, linked_stories, data)
            if len(steps) > 1:
                self.create_steps(story_id, title, steps, data)
        db.commit()

    def get_story(self, story_id):
        db = psycopg2.connect("host='127.0.0.1' dbname='postgres' user='postgres' password='password'")
        data = db.cursor()
        story_id = str(story_id)
        mysql = "SELECT * FROM USER_STORIES WHERE story_id = " + story_id
        data.execute(mysql)
        story_list = []
        temp = data.fetchone()
        for element in temp:
            story_list.append(element)
        # if 'user' in story_list[2]:
        #     role_name = self.get_role_name(data)
        #     story_list[2] = str(story_list[2]).replace("user", role_name).lower()
        mysql = "SELECT * FROM STEPS WHERE story_id = " + story_id
        data.execute(mysql)
        steps = data.fetchall()
        story_list.append(steps)
        mysql = "SELECT * FROM ASSUMPTIONS WHERE story_id = " + story_id
        data.execute(mysql)
        assumptions = data.fetchall()
        story_list.append(assumptions)
        story_list.append(self.role)
        return story_list

    @staticmethod
    def check_story(title):
        db = psycopg2.connect("host='127.0.0.1' dbname='postgres' user='postgres' password='password'")
        data = db.cursor()
        title = str(title)
        mysql = "SELECT * FROM USER_STORIES WHERE story_title='" + title + "'"
        data.execute(mysql)
        saved = data.fetchone()
        if saved:
            return True
        else:
            return False

    def get_containing_epics(self, story_id):
        db = psycopg2.connect("host='127.0.0.1' dbname='postgres' user='postgres' password='password'")
        data = db.cursor()
        story_id = str(story_id)
        containing_epics = []
        mysql = "SELECT * FROM USER_STORIES WHERE story_id=" + story_id
        data.execute(mysql)
        temp = data.fetchone()
        containing_epics.append(temp)
        if self.get_epic(temp[3], data) != 0:
            self.get_containing_epics(temp[0])
        return containing_epics

    @staticmethod
    def delete_story(story_id):
        db = psycopg2.connect("host='127.0.0.1' dbname='postgres' user='postgres' password='password'")
        data = db.cursor()
        story_id = str(story_id)
        mysql = "DELETE FROM USER_STORIES WHERE story_id='" + story_id + "'"
        data.execute(mysql)
        mysql = "DELETE FROM ROLE_STORIES WHERE story_id='" + story_id + "'"
        data.execute(mysql)
        mysql = "DELETE FROM STEPS WHERE story_id='" + story_id + "'"
        data.execute(mysql)
        mysql = "DELETE FROM ASSUMPTIONS WHERE story_id='" + story_id + "'"
        data.execute(mysql)

    def update_story(self, story):
        db = psycopg2.connect("host='127.0.0.1' dbname='postgres' user='postgres' password='password'")
        data = db.cursor()
        if story[3] == 'None' or story[3] == '':
            story[3] = None
        if story[4] == 'None' or story[4] == '':
            story[4] = None
        mysql = "UPDATE USER_STORIES SET story_title=%s, description=%s, containing_epic=%s, workflow_id=%s WHERE story_id='" + str(story[0]) + "'"
        data.execute(mysql, (story[1], story[2], story[3], story[4]))
        data.execute("DELETE FROM STEPS WHERE story_id = %s", str(story[0]))
        if len(story[5]) > 0:
            self.create_steps(story[0], story[1], story[5], data)
        data.execute("DELETE FROM ASSUMPTIONS WHERE story_id = %s", str(story[0]))
        if len(story[6]) > 0:
            self.create_assumptions(story[0], story[6], story[7], data)
        if len(story[8]) > 0:
            mysql = "DELETE FROM ROLE_STORIES WHERE ROLE_STORIES.story_id='" + str(story[0]) + "'"
            data.execute(mysql)
            self.create_role_story(story[8], story[0], data)
        db.commit()
