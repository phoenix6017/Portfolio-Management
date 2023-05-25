from flask import Flask, render_template, request, redirect, flash,session, jsonify
from db import login,signupinsert,logout
from functools import wraps
def login_required_for_id(f):
    @wraps(f)
    def decorated_function(id, *args, **kwargs):
        if 'username' not in session or session['username'] != id:
            return redirect('/login')
        return f(id, *args, **kwargs)
    return decorated_function

app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route("/")
def hello():
  if 'username' in session:
          return redirect('/user/{}'.format(session['username']))
  return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login_page():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    result = login(username, password)
    if result == "Welcome":
      session['username'] = username
      return redirect('/user/{}'.format(username))
    else:
      flash(result, 'error')
  return render_template('login.html')
@app.route("/logout")
def logout_page():
    logout(session['username'])
    session.pop('username', None)
    return redirect('/')
  
@app.route("/user/<id>")
@login_required_for_id
def data_page(id):
  return render_template('index.html',username = id)
@app.route("/user/<id>/temp")
@login_required_for_id
def temp(id):
   return render_template('temp.html',username= id)

@app.route("/user/<id>/payment")
@login_required_for_id
def pay(id):
   return render_template('paymentPage.html',username=id)
@app.route("/user/<id>/success")
@login_required_for_id
def success(id):
   return render_template('successPage.html',username=id)
@app.route("/register",methods=['GET','POST'])
def signup():
  print("ok")
  if request.method=='POST':
    print("doing it")
    data=request.form
    result=signupinsert(data)
    print(result)
    if result == "Success":
      return redirect('/login')
    else:
      flash(result, 'error')
  return render_template('register.html')
if __name__=="__main__":
  app.run(host='0.0.0.0',debug=True)
