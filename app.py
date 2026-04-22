from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- DATABASE ---------------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    type = db.Column(db.String(50))
    category = db.Column(db.String(100))
    amount = db.Column(db.Float)

# ---------------- ROUTES ---------------- #

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username'],
            password=request.form['password']
        ).first()

        if user:
            session['user_id'] = user.id
            return redirect('/dashboard')
        else:
            return "Invalid Login"

    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        new_user = User(
            username=request.form['username'],
            password=request.form['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')

    return render_template('register.html')


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    if request.method == 'POST':
        new_data = Expense(
            user_id=session['user_id'],
            type=request.form['type'],
            category=request.form['category'],
            amount=float(request.form['amount'])
        )
        db.session.add(new_data)
        db.session.commit()

    data = Expense.query.filter_by(user_id=session['user_id']).all()

    income = sum(x.amount for x in data if x.type == 'income')
    expense = sum(x.amount for x in data if x.type == 'expense')
    balance = income - expense

    warning = None
    if balance < 500:
        warning = "⚠️ Low Balance!"

    # -------- CHART DATA -------- #
    categories = {}
    for x in data:
        if x.type == 'expense':
            categories[x.category] = categories.get(x.category, 0) + x.amount

    return render_template('dashboard.html',
                           income=income,
                           expense=expense,
                           balance=balance,
                           warning=warning,
                           data=data,
                           categories=categories)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)