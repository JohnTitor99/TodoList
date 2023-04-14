from flask import render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user

from app import app, db, bcrypt
from models import User, Task
from forms import RegisterForm, LoginForm, AddForm

#! setunp a database
# > set FLASK_APP=views
# > flask shell
# > from app import app, db
# > from models import User, Task...
# > db.drop_all()
# > db.create_all()

#! update tables
# > db.drop_all()
# > db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main_page'))
            else:
                return "Username or password is incorrect."
        else:
            return "Username or password is incorrect."
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main_page'))

    return render_template('register.html', form=form)


@app.route('/')
@login_required
def main_page():
    search = request.args.get('q')
    if not search:
        tasks = Task.query.filter_by(user_id=current_user.id)
    else:
        tasks = Task.query.filter_by(user_id=current_user.id).filter(Task.title.contains(search))

    uncompleted_tasks = Task.query.filter_by(completed=False).count()

    context = {
        'tasks': tasks,
        'uncompleted_tasks': uncompleted_tasks,
    }
    
    return render_template('main_page.html', **context)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        new_task = Task(user_id=current_user.id, title=title, description=description)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
        
    context = {
        'form': form
    }
        
    return render_template('add.html', **context)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    task = Task.query.get_or_404(id)
    tasks = Task.query.all()

    if request.method == 'POST':
        if 'update-form' in request.form:
            task.title = request.form['title-update']
            task.description = request.form['des-update']
            db.session.commit()
            return redirect('/')

    context = {
        'task': task,
        'tasks': tasks,
    }

    return render_template('details.html', **context)


@app.route('/complete/<int:id>')
@login_required
def complete(id):
    task = Task.query.get_or_404(id)
    if task.completed == False:
        task.completed = True
        db.session.commit()
    elif task.completed == True:
        task.completed = False
        db.session.commit()
    
    return redirect('/')


@app.route('/username_change', methods=['GET', 'POST'])
@login_required
def username_change():
    if request.method == 'POST':
        new_username = request.form['new-username']
        current_user.username = new_username
        db.session.commit()
        return redirect('/')

    return render_template('username_change.html')


@app.route('/password_change', methods=['GET', 'POST'])
@login_required
def password_change():
    if request.method == 'POST':
        old_password = request.form['old-password']
        new_password = request.form['new-password']
        confirm_new_password = request.form['confirm-new-password']
        if bcrypt.check_password_hash(current_user.password, old_password) and new_password == confirm_new_password:
            hashed_password = bcrypt.generate_password_hash(new_password)
            current_user.password = hashed_password
            db.session.commit()
        else:
            return "Your old password is wrong or password confirmation don't match with the new password."
        return redirect('/')
    return render_template('password_change.html')


if __name__ == "__main__":
    app.run(debug=True)