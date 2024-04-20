from flask import Flask, render_template, url_for, redirect, request, flash, send_from_directory, make_response
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_uploads import UploadSet, IMAGES, configure_uploads
from waitress import serve

from data import db_session
from data.users import User
from data.orders import Orders
from data.items import Items
from forms.user import LoginForm, RegisterForm
from forms.Item import AddItem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/buy/<int:id>")
def get_product(id):
    db_sess = db_session.create_session()
    item = db_sess.query(Items).filter(Items.article == id).first()
    return render_template('showoff.html', item=item)


@app.route("/", methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    items = db_sess.query(Items).filter().all()
    return render_template('test2.html', user=items)


@app.route('/registration', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect('/')
            else:
                flash('incorrect password!')
                return render_template('login2.html', form=form)
        else:
            flash('incorrect email!')
            return render_template('login2.html', form=form)
    return render_template("login2.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/uploads/<filename>")
def get_file(filename):
    return send_from_directory(app.config["UPLOADED_PHOTOS_DEST"], filename)


@app.route('/creator', methods=["POST", "GET"])
@login_required
def creator():
    form = AddItem()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
        db_sess = db_session.create_session()
        item = Items(name=form.item_name.data,
                     about=form.about.data,
                     price=form.price.data,
                     picture=file_url,
                     user_id=current_user.id,
                     )
        db_sess.merge(current_user)
        db_sess.add(item)
        db_sess.commit()
        return redirect("/")
    else:
        file_url = None
    return render_template("creator.html", form=form, file_url=file_url)


@app.route("/cart")
@login_required
def cart():
    db_sess = db_session.create_session()
    user_id = current_user.id
    cart_items = db_sess.query(Orders).filter_by(user_id=user_id).all()
    items = []
    final_total = 0
    for item in cart_items:
        item = db_sess.query(Items).get(item.item_id)
        final_total += int(item.price)
        items.append(item)
    return render_template('cart.html', cart=items, final_total=final_total)


@app.route('/<int:item_article>/add_to_cart', methods=["POST", "GET"])
def add_to_cart(item_article):
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        user_id = current_user.id
        cart_item = db_sess.query(Orders).filter_by(item_id=item_article, user_id=user_id).first()
        if not cart_item:
            cart_item = Orders(item_id=item_article, user_id=user_id,)
            db_sess.add(cart_item)
            db_sess.commit()
    else:
        flash('You need to log in to add items to your cart', category='danger')
        return redirect(url_for('login'))
    return redirect(url_for('cart'))


@app.route("/edit", methods=['GET', 'POST'])
@login_required
def edit():
    db_sess = db_session.create_session()
    items = db_sess.query(Items).filter(Items.user_id == current_user.id ).all()
    return render_template("user_edit.html", user=items)


@app.route("/edit/delete/<int:item_article>")
@login_required
def delete(item_article):
    db_sess = db_session.create_session()
    items = db_sess.query(Items).filter(Items.article == item_article).first()
    db_sess.delete(items)
    db_sess.commit()
    return redirect(url_for('edit'))


@app.route('/cart/<int:item_article>/remove', methods=["POST", "GET"])
def remove_from_cart(item_article):
    db_sess = db_session.create_session()
    user_id = current_user.id
    cart_item = db_sess.query(Orders).filter_by(item_id=item_article, user_id=user_id).first()
    if not cart_item:
        return redirect(url_for('cart'))
    db_sess.delete(cart_item)
    db_sess.commit()
    return redirect(url_for('cart'))


@app.route("/cart/clear")
def clear():
    db_sess = db_session.create_session()
    user_id = current_user.id
    cart_items = db_sess.query(Orders).filter_by(user_id=user_id).all()
    for elem in cart_items:
        db_sess.delete(elem)
    db_sess.commit()
    return redirect(url_for('cart'))


@app.route('/payment')
@login_required
def payment():
    db_sess = db_session.create_session()
    user_id = current_user.id
    cart_items = db_sess.query(Orders).filter_by(user_id=user_id).all()
    items = [str(user_id)]
    total_sum = 0
    for item in cart_items:
        item_obj = db_sess.query(Items).get(item.item_id)
        total_sum += int(item_obj.price)
        items.append(str(item_obj.article))
    return render_template('payment.html', order_id=''.join(items), total_sum=total_sum)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
