from app import app, Message, mail
from flask import render_template, request, redirect, url_for, flash
from app.forms import UserInfoForm, PostForm, LoginForm
from app.models import User, Post
from flask_login import login_required,login_user, current_user,logout_user

# Home Route
@app.route('/')
def home():
    posts = Post.query.all()
    return render_template("home.html", posts = posts)

# Register Route
@app.route('/register', methods=['GET','POST'])
def register():
    form = UserInfoForm()
    if form.validate_on_submit():
        # Get Information
        username = form.username.data
        password = form.password.data
        email = form.email.data
        # Create an instance of User
        User(username=username,email=email,password=password)
        # Flask Email Sender 
        # msg = Message(f'Thanks for Signing Up! {username}', sender="joelc@doubleedgesoftware.com", recipients=[email])
        # msg.body = ('Congrats on signing up! Looking forward to your posts!')
        # msg.html = ('<h1> Welcome to debug_project_app!</h1> <p> This will be fun! </p>')
        # mail.send(msg)
        flash("The new user has been created","success")
        return redirect(url_for('home'))
    return render_template('register.html',form = form)

# Post Submission Route
@app.route('/posts', methods=['GET','POST'])
@login_required
def posts():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id
        Post(title,content,user_id=user_id)
        flash(f"{title} has been created", 'secondary')
        return redirect(url_for('home'))
    return render_template('posts.html', form=form)

@app.route('/posts/<post_id>')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)


@app.route('/posts/update/<post_id>', methods = ['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash("You don't have permission to edit this post","danger")
        return redirect(url_for('home'))
    update_form = PostForm()
    if update_form.validate_on_submit():
        title = update_form.title.data
        content = update_form.content.data
        user_id = current_user.id
        post = post.update(title=title, content=content, user_id=user_id)
        flash(f'{title} has been updated', 'success')
        return redirect(url_for('home'))
    return render_template('post_update.html', update_form=update_form, post=post)

@app.route('/posts/delete/<post_id>')
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash("You don't have permission to delete this post","danger")
        return redirect(url_for('home'))
    post.delete()
    flash(f'{post.title} has been deleted','info')
    return redirect(url_for('home'))

# Login Form Route
@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        logged_user = User.query.filter(User.email == email).first()
        print("user pass",logged_user.check_password(password))
        if logged_user and logged_user.check_password(password):
            login_user(logged_user)
            flash(f"Hi {logged_user.username}","success")
            return redirect(url_for('home'))
        else:
            flash("Incorrect credential","danger")
            return redirect(url_for('login'))

    return render_template('login.html',form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))