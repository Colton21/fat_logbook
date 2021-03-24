from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
#from guess_language import guess_language
from app import db
from app.main.forms import EditProfileForm, PostForm, SearchForm, MessageForm
from app.main.forms import ChecklistForm, StartShiftForm, EndShiftForm, FreezerForm, StartRunForm
from app.models import User, Post, Message, Notification, StartShiftPost, EndShiftPost
from app.models import ChecklistPost, FreezerPost, StartRunPost
from app.translate import translate
from app.main import bp

import numpy as np

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    make_post = url_for('main.post_choice', title='New Logbook Entry')
    language='en'

    form = PostForm()
    if form.validate_on_submit():
        #language =guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Update Posted to Logbook'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Home'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/post_choice')
@login_required
def post_choice():
    start_shift = url_for('main.start_shift')
    return render_template('post_choice.html', title=('New Logbook iPost'), start_shift=start_shift)

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        language = 'en'
        #language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, module_id=form.module_id.data, sw_hw=form.sw_hw.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Update Posted to Logbook'))
        return redirect(url_for('main.index'))
    return render_template('new_post.html', title='Logbook Entry', form=form)

@bp.route('/start_shift', methods=['GET', 'POST'])
@login_required
def start_shift():
    form = StartShiftForm()
    if form.validate_on_submit():
        post = StartShiftPost(body=form.post.data, run_id=form.run_id.data, author=current_user)
        #post = StartShiftPost(runid=form.run_id.data)
        db.session.add(post)
        db.session.commit()
        flash(f'Shift started for {current_user}')
        return redirect(url_for('main.index'))
    return render_template('start_shift.html', title='Start of Shift', form=form)

@bp.route('/start_run', methods=['GET', 'POST'])
@login_required
def start_run():
    form = StartRunForm()
    if form.validate_on_submit():
        post = StartRunPost(body=form.post.data, run_id=form.run_id.data, module_ids=form.module_ids.data,
                               function_gen=form.function_gen.data, laser=form.laser.data,
                               thermos=form.thermos.data, humidity=form.humidity.data,
                               fw_wheel=form.fw_wheel.data, setup=form.setup.data,
                               flash=form.flash.data, configs=form.configs.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('New Run Started')
        return redirect(url_for('main.index'))
    return render_template('start_shift.html', title='Start New Run', form=form)

@bp.route('/end_shift', methods=['GET', 'POST'])
@login_required
def end_shift():
    form = EndShiftForm()
    if form.validate_on_submit():
        post = EndShiftPost(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Shift ended for {current_user}')
        return redirect(url_for('main.index'))
    return render_template('end_shift.html', title='End of Shift', form=form)

@bp.route('/checklist', methods=['GET', 'POST'])
@login_required
def checklist():
    form = ChecklistForm()
    if form.validate_on_submit():
        post = ChecklistPost(body=form.post.data, running=form.running.data, slack=form.slack.data,
                    temperature=form.temp.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Shifter Checklist')
        return redirect(url_for('main.index'))
    return render_template('checklist.html', title='Shifter Checklist', form=form)

@bp.route('/freezer_form', methods=['GET', 'POST'])
@login_required
def freezer_form():
    form = FreezerForm()
    if form.validate_on_submit():
        post = FreezerPost(body=form.post.data, hv=form.hv.data, laser=form.laser.data,
                    freezer_temp_s=form.freezer_temp_s.data,
                    freezer_temp_e=form.freezer_temp_e.data,
                    freezer_hum_s=form.freezer_hum_s.data,
                    freezer_hum_e=form.freezer_hum_e.data,
                    start=form.start.data,
                    end=form.end.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Freezer Access for {current_user}')
        return redirect(url_for('main.index'))
    return render_template('freezer_form.html', title='Freezer Access Form', form=form)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/upload', methods=['GET', 'POST'])
def upload(slowmon_data):
  with open(slowmon_data, "r") as f:
    content = f.read()
  splt = content.split(",")  
  timestamp = strptime(splt[0])
  room_temp = float(splt[1])
  freezer_temp = float(splt[2])

  newFile = SlowMonPost(timestamp=timestamp, room_temp=room_temp, freezer_temp=freezer_temp)
  db.session.add(newFile)
  db.session.commit()

  flash('SlowMon Database Updated')
  return redirect(url_for('main.index'))

@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', title=_('Send Message'),
                           form=form, recipient=recipient)


@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/export_posts')
@login_required
def export_posts():
    if current_user.get_task_in_progress('export_posts'):
        flash(_('An export task is currently in progress'))
    else:
        current_user.launch_task('export_posts', _('Exporting posts...'))
        db.session.commit()
    return redirect(url_for('main.user', username=current_user.username))


@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])
