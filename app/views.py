from os.path import join, dirname, realpath, isfile
import docx
from werkzeug.utils import secure_filename
from flask import render_template, redirect, request, url_for, flash
from app import app
from databaseManager import DatabaseManager
import boto3
db = DatabaseManager()
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/images/uploads_full/')
DOWNLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/images/downloads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['CURRENT_ROLE'] = 0
epics = db.get_all_epics()
stories = db.get_all_stories()
s3 = boto3.client(
    's3',
    aws_access_key_id=app.config['KEY_ID'],
    aws_secret_access_key=app.config['KEY_ACCESS'],
)


@app.route('/')
def start():
    roles = db.get_roles()
    db.clear_role()
    return render_template('home.html', roles=roles)


@app.route('/roles_home')
def save_role():
    db.set_role(int(request.args.get('role', None)))
    return redirect(url_for('.role_home'))


@app.route('/role_home')
def role_home():
    try:
        current_role = app.config['CURRENT_ROLE']
    except KeyError:
        current_role = 0
    if current_role is not 0:
        stories_in_role = db.get_stories('0', current_role)
        return render_template('rolehome.html', stories=stories_in_role)
    else:
        return redirect(url_for('.start'))


@app.route('/add_story', methods=['GET', 'POST'])
def add_story():
    if request.method == 'POST':
        role = request.form['roleSelect']
        epic_title = request.form['epic_title']
        title = request.form['title']
        description = request.form['description']
        assumptions = request.form.getlist('assumption')
        steps = request.form.getlist("step")
        return render_template('addstory.html', role=role, epic_title=epic_title, title=title,
                               description=description, assumptions=assumptions, steps=steps)
    else:
        return render_template('addstory.html', stories=stories, epic_list=epics)


@app.route('/upload', methods=['GET', 'POST'])
def upload_story():
    epics = db.get_all_epics()
    stories = db.get_all_stories()
    db.clear_role()
    if request.method == 'POST':
        args = request.args.to_dict()
        try:
            story = args['story']
        except KeyError:
            story = 0
        try:
            edit = args['edit']
        except KeyError:
            edit = 'False'
        role1 = request.form.getlist('role_check_1')
        role2 = request.form.getlist('role_check_2')
        role3 = request.form.getlist('role_check_3')
        roles = [role1, role2, role3]
        for i, role in enumerate(roles):
            if role:
                roles[i] = 'checked'
            else:
                roles[i] = ''
        epic_title = request.form['epic_title']
        title = request.form['title']
        description = request.form['description']
        assumptions = request.form.getlist('assumption')
        linked_stories = request.form.getlist('assumption_link')
        workflow = request.form['workflow_num']
        steps = request.form.getlist("step")
        files = request.files.getlist("step")
        for file in files:
            filename = secure_filename(file.filename)
            filename = str(title).replace(" ", "_").lower() + "_" + filename
            saved = isfile(app.config['UPLOAD_FOLDER'] + filename)
            if not saved:
                file.save(join(app.config['UPLOAD_FOLDER'], filename))
                file_location = app.config['UPLOAD_FOLDER'] + filename
                key = 'static/images/downloads/' + filename
                s3.upload_file(file_location, "processflowc5", key)
        story_saved = db.check_story(title)
        if edit == 'False':
            if story_saved:
                flash('This story title has already been used')
                return render_template('addstory.html', roles=roles, epic_title=epic_title, title=title,
                                       description=description, assumption_list=zip(assumptions, linked_stories),
                                       epic_list=epics, stories=stories, steps=steps)
            flash('The story was successfully saved')
            db.save_story(roles, epic_title, title, description, assumptions, linked_stories, workflow, steps)
            return redirect(url_for('add_story'))
        elif edit == 'True':
            story_to_update = [story, title, description, epic_title, workflow, steps, assumptions, linked_stories, roles]
            db.update_story(story_to_update)
            flash('The story has been updated successfully')
            # return render_template('addstory.html', roles=roles, epic_title=epic_title, title=title,
            #                        description=description, assumption_list=zip(assumptions, linked_stories),
            #                        epic_list=epics, stories=stories, steps=steps)
            db.set_role(4)
            story_list = db.get_story(story)
            return redirect(url_for('.get_story', story=story_list[0], edit=False))


@app.route('/stories_home')
def get_story():
    epics = db.get_all_epics()
    stories = db.get_all_stories()
    args = request.args.to_dict()
    story = args['story']
    try:
        edit = args['edit']
    except KeyError:
        edit = 'False'
    story_list = db.get_story(story)
    if edit == 'True':
        db.clear_role()
        story_list = db.get_story(story)
        assumptions = []
        links = []
        for i, assumption_list in enumerate(story_list[6]):
            assumptions.append(story_list[6][i][2])
            try:
                links.append(db.get_story(story_list[6][i][3])[1])
            except TypeError:
                links.append("")
        return render_template('addstory.html', roles=story_list[-1], epic_title=story_list[3], title=story_list[1],
                               description=story_list[2], assumption_list=zip(assumptions, links), steps=story_list[5],
                               id=story_list[0], stories=stories, epic_list=epics)
    epic = False
    current_stories = []
    containing_epics = []
    if story_list[5].__len__() == 0:
        epic = True
        current_stories = db.get_stories(story_list[1], app.config['CURRENT_ROLE'])
    if story_list[3] is not None:
        containing_epics = db.get_containing_epics(story_list[3])
    for step in story_list[5]:
        if step[2] == 3:
            image_name = str(step[3]).replace("%2F", "/")
            downloaded = isfile(image_name)
            if not downloaded:
                try:
                    s3.download_file("processflowc5", image_name, join(dirname(realpath(__file__)), image_name))
                except:
                    flash("Image " + image_name + " was not found")
    return render_template('storywalkthroughbase.html', story_list=story_list, epic=epic,
                           stories=current_stories, containing_epics=containing_epics)


@app.route('/delete', methods=['GET'])
def delete_story():
    if request.method == 'GET':
        args = request.args.to_dict()
        story = args['story']
        db.delete_story(story)
        flash("Story successfully deleted")
    return redirect(url_for('.start'))


@app.route('/help')
def get_help():
    return render_template('help.html')

