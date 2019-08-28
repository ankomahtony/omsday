import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm,
                             PastorForm, ChurchForm,SermonForm, UpEventForm,
                             DonationForm, QuoteForm, CommentForm,PastProgramForm)
from flaskblog.models import User, Post, Pastor, Church, Quote, UpEvent, Donation, Comment,Sermon,Past_P
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page',1,type=int)
    last_donation = Donation.query.order_by(Donation.id.desc()).first()
    pastor = Pastor.query.order_by(Pastor.id.desc()).first()
    church = Church.query.order_by(Church.id.desc()).first()
    sermon = Sermon.query.order_by(Sermon.id.desc()).first()
    quote = Quote.query.order_by(Quote.id.desc()).first()
    sermons = Sermon.query.order_by(Sermon.id.desc()).paginate(page=page, per_page=6)
    upevents = UpEvent.query.order_by(UpEvent.id.desc()).paginate(page=page, per_page=6)
    donations = Donation.query.order_by(Donation.id.desc()).paginate(page=page, per_page=4)
    p_program = Past_P.query.order_by(Past_P.id.desc()).paginate(page=page, per_page=4)
    post = Post.query.order_by(Post.id.desc()).first()
    posts = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=6)
    churches = Church.query.order_by(Church.id.desc()).all()
    church_no=0
    for ch in churches:
        church_no += ch.members
    upevent = UpEvent.query.order_by(UpEvent.id.desc()).first()
    per_t=(last_donation.received / last_donation.target) * 100
    return render_template('main/index_2.html',title='Official Website',church_no = church_no,per_t=per_t,p_program=p_program,posts=posts,quote=quote,donations=donations,upevents=upevents,sermons=sermons,upevent=upevent,post=post,sermon=sermon,church=church,last_donation=last_donation,pastor=pastor)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_picture_full(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    form_picture.save(picture_path)

    return picture_fn

def save_video(form_video):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_video.filename)
    video_fn = random_hex + f_ext
    video_path = os.path.join(app.root_path, 'static/videos', video_fn)

    form_video.save(video_path)

    return video_fn


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        picture_file = save_picture(form.picture.data)
        user = User(title=form.title.data, full_name=form.full_name.data, username=form.username.data, email=form.email.data,dob=form.dob.data,church=form.church.data, image_file=picture_file, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('{} has been created! You are now able to log in'.format(user.username), 'success')
        return redirect(url_for('login'))
    return render_template('main/register_new.html', title='Register', form=form)

@app.route("/church/new", methods=['GET', 'POST'])
def church_new():
    form = ChurchForm()
    if form.validate_on_submit():
        church = Church(name=form.name.data, est=form.est.data,loc=form.loc.data,members=form.members.data,image_file=save_picture_full(form.picture.data))
        db.session.add(church)
        db.session.commit()
        flash('{} Church is added to the database'.format(church.name))
        return redirect(url_for('home'))
    return render_template('main/church_new.html',title='Register your church',form=form)

@app.route("/pastor/new", methods=['GET', 'POST'])
def pastor_new():
    form = PastorForm()
    if form.validate_on_submit():
        pastor = Pastor(name= form.name.data, email= form.email.data, dob = form.dob.data,wife = form.wife.data,wife_image=save_picture(form.wife_picture.data), image_file=save_picture(form.picture.data),bio=form.bio.data)
        db.session.add(pastor)
        db.session.commit()
        flash('Pastor {} is registered'.format(pastor.name), 'success')
        return redirect(url_for('home'))
    return render_template('main/pastor_new.html',title='Register your pastor',form=form)

@app.route("/sermon/new", methods=['GET', 'POST'])
@login_required
def sermon_new():
    form = SermonForm()
    if form.validate_on_submit():
        sermon = Sermon(title=form.title.data,subtitle=form.subtitle.data,message=form.message.data,image_file=save_picture_full(form.picture.data),video_file=save_video(form.video.data),category = form.category.data)
        db.session.add(sermon)
        db.session.commit()
        flash('New sermon added')
        return redirect(url_for('home'))
    return render_template('main/sermon_new.html',title='Register your sermon',form=form)

@app.route("/sermon/<int:sermon_id>",methods=['GET','POST'])
def sermon(sermon_id):
    page = request.args.get('page',1,type=int)
    sermons = Sermon.query.order_by(Sermon.date_posted.desc()).paginate(page=page, per_page=5)
    sermon = Sermon.query.get_or_404(sermon_id)
    comments = Comment.query.order_by(Comment.date_posted.desc()).all()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comment=form.message.data,author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted!', 'success')
        return redirect(url_for('sermon',sermon_id=sermon.id))
    return render_template('main/single_vid.html', title=sermon.title, form=form,sermon=sermon, sermons=sermons, comments=comments)


@app.route("/sermon/<int:sermon_id>/update", methods=['GET', 'POST'])
@login_required
def update_sermon(sermon_id):
    page = request.args.get('page',1,type=int)
    sermons = Sermon.query.order_by(Sermon.date_posted.desc()).paginate(page=page, per_page=5)
    sermon = Sermon.query.get_or_404(sermon_id)
    if current_user.username != 'Admin':
        abort(403)
    form = SermonForm()
    if form.validate_on_submit():
        sermon.title = form.title.data
        sermon.subtitle = form.subtitle.data
        sermon.message = form.message.data
        sermon.category = form.category.data
        sermon.image_file = save_picture_full(form.picture.data)
        sermon.video_file = save_video(form.video.data)
        db.session.commit()
        flash('Your sermon has been updated!', 'success')
        return redirect(url_for('sermon', sermon_id=sermon.id))
    elif request.method == 'GET':
        form.title.data = sermon.title
        form.message.data = sermon.message
    return render_template('main/sermon_new.html', title='Update Sermon',
                           form=form, legend='Update Sermon',sermons=sermons)


@app.route("/sermon/<int:sermon_id>/delete", methods=['POST'])
@login_required
def delete_sermon(sermon_id):
    sermon = Sermon.query.get_or_404(sermon_id)
    if current_user.username != 'Admin':
        abort(403)
    db.session.delete(sermon)
    db.session.commit()
    flash('Your sermon has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/donation/new", methods=['GET', 'POST'])
def donation_new():
    form = DonationForm()
    if form.validate_on_submit():
        donation = Donation(title=form.title.data,target=form.target.data,received=form.received.data,message=form.message.data,image_file=save_picture_full(form.picture.data))
        db.session.add(donation)
        db.session.commit()
        flash('Donation Updated')
        return redirect(url_for('home'))
    return render_template('main/donation_new.html',title='Register your donation',form=form)

@app.route("/upevent/new", methods=['GET', 'POST'])
def upevent_new():
    form = UpEventForm()
    if form.validate_on_submit():
        upevent = UpEvent(event=form.event.data,start_time=form.start_time.data,end_time=form.end_time.data,loc=form.venue.data, image_file=save_picture_full(form.picture.data),facilatator=form.facilitator.data)
        db.session.add(upevent)
        db.session.commit()
        flash('New Event added')
        return redirect(url_for('home'))
    form = UpEventForm()
    return render_template('main/upevent_new.html',title='Register your Upcoming Event',form=form)

@app.route("/quote/new", methods=['GET', 'POST'])
def quote_new():
    form = QuoteForm()
    if form.validate_on_submit():
        quote = Quote(author=form.author.data,message=form.message.data,ref=form.ref.data)
        db.session.add(quote)
        db.session.commit()
        flash('Quote for the Day added')
        return redirect(url_for('home'))
    return render_template('main/quote_new.html',title='Quote of the Day',form=form)

@app.route("/past_program/new", methods=['GET', 'POST'])
def past_program():
    form = PastProgramForm()
    if form.validate_on_submit():
        past_program = Past_P(program=form.program.data,image_file=save_picture_full(form.picture.data))
        db.session.add(past_program)
        db.session.commit()
        flash('Past Program picture added')
        return redirect(url_for('home'))
    return render_template('main/past_program.html',title='Past Program Pictures',form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # page = request.args.get('page',1,type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('main/login_new.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    page = request.args.get('page',1,type=int)
    last_donation = Donation.query.order_by(Donation.id.desc()).first()
    pastor = Pastor.query.order_by(Pastor.id.desc()).first()
    church = Church.query.order_by(Church.id.desc()).first()
    sermon = Sermon.query.order_by(Sermon.id.desc()).first()
    quote = Quote.query.order_by(Quote.id.desc()).first()
    sermons = Sermon.query.order_by(Sermon.id.desc()).paginate(page=page, per_page=6)
    upevents = UpEvent.query.order_by(UpEvent.id.desc()).paginate(page=page, per_page=6)
    donations = Donation.query.order_by(Donation.id.desc()).paginate(page=page, per_page=4)
    p_program = Past_P.query.order_by(Past_P.id.desc()).paginate(page=page, per_page=4)
    post = Post.query.order_by(Post.id.desc()).first()
    posts = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=6)
    upevent = UpEvent.query.order_by(UpEvent.id.desc()).first()
    per_t=(last_donation.received / last_donation.target) * 100
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('main/account.html', title='Account',
                           image_file=image_file, form=form,posts=posts)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,subtitle=form.subtitle.data,category=form.category.data, content=form.content.data, image_file=save_picture_full(form.picture.data), author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('main/post_new.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>",methods=['GET','POST'])
def post(post_id):
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.order_by(Comment.date_posted.desc()).all()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comment=form.message.data,author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted!', 'success')
        return redirect(url_for('post',post_id=post.id))
    return render_template('main/single.html', title=post.title, form=form,post=post, posts=posts, comments=comments)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.image_file = save_picture_full(form.picture.data)
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.picture.data = post.image_file
    return render_template('main/post_new.html', title='Update Post',
                           form=form, legend='Update Post',posts=posts)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form, posts=posts)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form, posts=posts)


@app.route("/dashboard")
def dashboard():
    return render_template('main/dashboard.html', title='dashboard')

@app.route("/beliefs")
def beliefs():
    page = request.args.get('page',1,type=int)
    last_donation = Donation.query.order_by(Donation.id.desc()).first()
    pastor = Pastor.query.order_by(Pastor.id.desc()).first()
    church = Church.query.order_by(Church.id.desc()).first()
    sermon = Sermon.query.order_by(Sermon.id.desc()).first()
    quote = Quote.query.order_by(Quote.id.desc()).first()
    sermons = Sermon.query.order_by(Sermon.id.desc()).paginate(page=page, per_page=6)
    upevents = UpEvent.query.order_by(UpEvent.id.desc()).paginate(page=page, per_page=6)
    donations = Donation.query.order_by(Donation.id.desc()).paginate(page=page, per_page=4)
    post = Post.query.order_by(Post.id.desc()).first()
    posts = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=6)
    upevent = UpEvent.query.order_by(UpEvent.id.desc()).first()
    return render_template('main/beliefs.html',title='Fundamental Beliefs',posts=posts,quote=quote,donations=donations,upevents=upevents,sermons=sermons,upevent=upevent,post=post,sermon=sermon,church=church,last_donation=last_donation,pastor=pastor)

@app.route("/fellowships")
def fellowships():
    page = request.args.get('page',1,type=int)
    last_donation = Donation.query.order_by(Donation.id.desc()).first()
    pastor = Pastor.query.order_by(Pastor.id.desc()).first()
    church = Church.query.order_by(Church.id.desc()).first()
    sermon = Sermon.query.order_by(Sermon.id.desc()).first()
    quote = Quote.query.order_by(Quote.id.desc()).first()
    sermons = Sermon.query.order_by(Sermon.id.desc()).paginate(page=page, per_page=6)
    upevents = UpEvent.query.order_by(UpEvent.id.desc()).paginate(page=page, per_page=6)
    donations = Donation.query.order_by(Donation.id.desc()).paginate(page=page, per_page=4)
    post = Post.query.order_by(Post.id.desc()).first()
    posts = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=6)
    upevent = UpEvent.query.order_by(UpEvent.id.desc()).first()
    return render_template('main/fellowships.html',title='Fundamental Fellowships',posts=posts,quote=quote,donations=donations,upevents=upevents,sermons=sermons,upevent=upevent,post=post,sermon=sermon,church=church,last_donation=last_donation,pastor=pastor)
