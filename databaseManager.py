from app import app, models, db_create, db


class DatabaseManager:
    role = ''
    approved_files = ['.gif', '.GIF']

    def __init__(self):
        db_create.init_database()
        pass

    @staticmethod
    def clear_role():
        app.config['CURRENT_ROLE'] = 0

    @staticmethod
    def set_role(role_num):
        app.config['CURRENT_ROLE'] = role_num

    @staticmethod
    def get_role_name(role_num):
        if role_num == 0:
            return "a user"
        role = models.Roles.query.filter(models.Roles.id == role_num).first()
        role_name = role.role_name
        if role_name == "Other" or role_name == "Index":
            role_name = "an Application User"
        else:
            role_name = "a " + role_name
        return role_name

    @staticmethod
    def get_roles():
        roles = models.Roles.query.all()
        role_list = []
        if roles:
            for role in roles:
                role_list.append([role.role_name, role.id])
            return role_list
        else:
            return 0

    @staticmethod
    def get_all_stories():
        temp = models.Stories.query.order_by(models.Stories.story_title.asc()).all()
        stories = []
        for story in temp:
            stories.append(story.story_title)
        return stories

    @staticmethod
    def get_all_epics():
        temp = models.Stories.query.all()
        epics = []
        for story in temp:
            story_id = story.id
            steps = models.Steps.query.filter(models.Steps.story_id == story_id).count()
            if steps == 0:
                epics.append(story.story_title)
        return epics

    def get_stories(self, epic, role):
        story_list = []
        current_role = role
        current_role_name = self.get_role_name(current_role)
        if epic == '0':
            if current_role is not 0:
                if current_role == 4:
                    temp = models.Stories.query.order_by(models.Stories.story_title.asc())
                    temp.all()
                    stories = []
                    for story in temp:
                        story_id = story.id
                        steps = models.Steps.query.filter(models.Steps.story_id == story_id).count()
                        if steps != 0:
                            role_description = str(story.description).replace("a user", current_role_name)
                            stories.append([story.id, story.story_title, role_description, story.containing_epic])
                    return stories
                role_stories = models.RoleStories.query.filter(models.RoleStories.role_id == current_role)
                role_stories.all()
                story_list = []
                for role_story in role_stories:
                    temp = models.Stories.query.filter(models.Stories.id == role_story.story_id).order_by(models.Stories.story_title.asc()).all()
                    for story in temp:
                        role_description = str(story.description).replace("a user", current_role_name)
                        story_list.append([story.id, story.story_title, role_description, story.containing_epic, story.workflow_id])
        else:
            temp = models.Stories.query.filter(models.Stories.containing_epic == epic).order_by(models.Stories.story_title.asc())
            temp.all()
            story_list = []
            if temp:
                for story in temp:
                    role_description = str(story.description).replace("a user", current_role_name)
                    story_list.append([story.id, story.story_title, role_description, story.containing_epic, story.workflow_id])
        return story_list

    @staticmethod
    def get_epic(epic_title):
        epic_title = str(epic_title)
        epic_id = models.Stories.query.filter(models.Stories.story_title == epic_title).first()
        if epic_id:
            return epic_id.id
        else:
            return 0

    @staticmethod
    def create_user_story(name, description, workflow, epic_title):
        name = str(name)
        description = str(description)
        if epic_title == 0 or epic_title is None:
            epic_title = None
        else:
            epic_title = str(epic_title)
        if workflow == '' or workflow is None:
            workflow = None
        else:
            workflow = str(workflow)
        userstory_id = 0
        if name != '':
            if description != '':
                try:
                    new_story = models.Stories(story_title=name, description=description, containing_epic=epic_title, workflow_id=workflow)
                    db.session.add(new_story)
                    db.session.commit()
                    userstory_id = models.Stories.query.filter(models.Stories.story_title == name).first()
                    userstory_id = userstory_id.id
                except SystemError:
                    return "This story already exists"
        return userstory_id

    @staticmethod
    def create_assumptions(story_id, assumptions, links):
        if assumptions:
            for i, assumption in enumerate(assumptions):
                assumption = str(assumption)
                if len(links[i]) > 1:
                    temp = models.Stories.query.filter(models.Stories.story_title == str(links[i])).first()
                    link = temp.id
                else:
                    link = None
                new_assumption = models.Assumptions(story_id=story_id, assumption=assumption, containing_id=link)
                db.session.add(new_assumption)
            db.session.commit()

    def create_steps(self, story_id, story_title, steps):
        step_num = 1
        if steps:
            for step in steps:
                step = str(step)
                if any(x in step for x in self.approved_files):
                    if "static%2Fimages%2Fdownloads%2F" not in step:
                        step = "static/images/downloads/" + str(story_title).replace(" ", "_").lower() + "_" + step
                    step_type = 3
                elif step[0] == "(":
                    step_type = 2
                else:
                    step_type = 1
                new_step = models.Steps(story_id=story_id, type=step_type, content=step, step_num=step_num)
                db.session.add(new_step)
                step_num += 1
            db.session.commit()

    @staticmethod
    def create_role_story(roles, story_id):
        story_id = str(story_id)
        role_num = 1
        for role in roles:
            if role == 'checked':
                role_id = role_num
                new_role = models.RoleStories(role_id=role_id, story_id=story_id)
                db.session.add(new_role)
            role_num += 1
        db.session.commit()

    def save_story(self, roles, epic_title, title, description, assumptions, linked_stories, workflow, steps):
        story_id = self.create_user_story(title, description, workflow, epic_title)
        if story_id != 0:
            self.create_role_story(roles, story_id)
            if assumptions:
                self.create_assumptions(story_id, assumptions, linked_stories)
            if len(steps) > 1:
                self.create_steps(story_id, title, steps)
        db.session.commit()

    def get_story(self, story_id):
        story_list = []
        story_id = int(story_id)
        temp = models.Stories.query.filter(models.Stories.id == story_id).first()
        story_list.append(temp.id)
        story_list.append(temp.story_title)
        try:
            current_role = self.get_role_name(app.config['CURRENT_ROLE'])
        except KeyError:
            current_role = "an Application User"
        role_description = str(temp.description).replace("a user", current_role)
        story_list.append(role_description)
        story_list.append(temp.containing_epic)
        story_list.append(temp.workflow_id)
        steps = models.Steps.query.filter(models.Steps.story_id == story_id).all()
        temp = []
        for step in steps:
            temp.append([step.id, step.story_id, step.type, step.content, step.step_num])
        story_list.append(temp)
        assumptions = models.Assumptions.query.filter(models.Assumptions.story_id == story_id).all()
        temp = []
        for assumption in assumptions:
            temp.append([assumption.id, assumption.story_id, assumption.assumption, assumption.containing_id])
        story_list.append(temp)
        roles = models.RoleStories.query.filter(models.RoleStories.story_id == story_id).all()
        temp = [0, 0, 0]
        for role in roles:
            temp[role.role_id - 1] = "checked"
        story_list.append(temp)
        return story_list

    @staticmethod
    def check_story(title):
        saved = models.Stories.query.filter(models.Stories.story_title == title).first()
        if saved:
            return True
        else:
            return False

    def get_containing_epics(self, story_title):
        if story_title == '':
            return []
        containing_epics = []
        if isinstance(story_title, str):
            temp = models.Stories.query.filter(models.Stories.story_title == story_title).first()
        elif isinstance(story_title, int):
            temp = models.Stories.query.filter(models.Stories.id == story_title).first()
        containing_epics.append([temp.id, temp.story_title, temp.description, temp.containing_epic])
        if self.get_epic(temp.containing_epic) != 0:
            self.get_containing_epics(temp.id)
        return containing_epics

    @staticmethod
    def delete_story(story_id):
        story_id = int(story_id)
        old_role_stories = models.RoleStories.query.filter(models.RoleStories.story_id == story_id)
        old_role_stories.all()
        for old_role_story in old_role_stories:
            db.session.delete(old_role_story)
        old_steps = models.Steps.query.filter(models.Steps.story_id == story_id)
        old_steps.all()
        for old_step in old_steps:
            db.session.delete(old_step)
        old_assumptions = models.Assumptions.query.filter(models.Assumptions.story_id == story_id)
        old_assumptions.all()
        for old_assumption in old_assumptions:
            db.session.delete(old_assumption)
        old_story = models.Stories.query.filter(models.Stories.id == story_id).first()
        db.session.delete(old_story)
        db.session.commit()

    def update_story(self, story):
        if story[3] == 'None' or story[3] == '':
            story[3] = None
        if story[4] == 'None' or story[4] == '':
            story[4] = None
        old_story = models.Stories.query.filter(models.Stories.id == story[0]).first()
        old_story.story_title = story[1]
        old_story.description = story[2]
        old_story.containing_epic = story[3]
        old_story.workflow_id = story[4]
        old_steps = models.Steps.query.filter(models.Steps.story_id == story[0])
        old_steps.all()
        for old_step in old_steps:
            db.session.delete(old_step)
        if len(story[5][0]) > 0:
            self.create_steps(story[0], story[1], story[5])
        old_assumptions = models.Assumptions.query.filter(models.Assumptions.story_id == story[0])
        old_assumptions.all()
        for old_assumption in old_assumptions:
            db.session.delete(old_assumption)
        if len(story[6]) > 0:
            self.create_assumptions(story[0], story[6], story[7])
        if len(story[8]) > 0:
            old_roles = models.RoleStories.query.filter(models.RoleStories.story_id == story[0])
            old_roles.all()
            for old_role in old_roles:
                db.session.delete(old_role)
            self.create_role_story(story[8], story[0])
        db.session.commit()
