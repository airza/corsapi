from flask import Flask, session,url_for,redirect,request,render_template,Response,jsonify
from functools import wraps
from utils import *
import json 
import os
app = Flask(__name__)

def login_required(f):
    @wraps(f)
    def loginRequired(*args,**kwargs):
        user = 'username' in session and session['username']
        print '????'
        if not user:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return loginRequired

@app.route('/login', methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
    if valid_login(request.form['username'],request.form['password']):
      session['username'] = request.form['username']
      return redirect(url_for("index"))
    else:
      return redirect(url_for("login"))
  else:
      return render_template("login.html")

@app.route('/',methods=['GET'])
@login_required
def index():
    print('required?')
    return render_template("index.html")

@app.route("/basic_api",methods=['get'])
@login_required
def basicApi():
    user_data = return_record(session['username'])
    return jsonify(user_data)

@app.route("/star_api",methods=['get'])
@login_required
def starApi():
    headers= {
      'Access-Control-Allow-Origin':'*'
    }
    data=json.dumps(return_record(session['username']))
    response = Response(response=data,headers=headers)
    return response

@app.route("/star_credentials_api",methods=['get'])
@login_required
def starCredentialsApi():
    headers= {
      'Access-Control-Allow-Origin':'*',
      'Access-Control-Allow-Credentials': True
    }
    data=json.dumps(return_record(session['username']))
    response = Response(response=data,headers=headers)
    return response


@app.route("/awful_api",methods=['get'])
@login_required
def awfulApi():
    origin = request.headers['origin'] if 'origin' in request.headers else 'sameorigin'

    headers= {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Credentials': True
    }
    data=json.dumps(return_record(session['username']))
    response = Response(response=data,headers=headers)
    return response

@app.route("/jsonp_api",methods=['get'])
@login_required
def jsonPApi():
    callback = request.args.get('callback', '')
    data=callback+"(%s)"%json.dumps(return_record(session['username']))
    return data,200,{"Content-Type":"application/javascript; charset=utf-8"}

@app.route("/logout",methods=['get'])
def logout():
  if 'username' in session:
    del session['username']
  return 'ok'

app.secret_key="248135829013891840918-4182-481-4809358029385082350923849184-32842835902035"
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
