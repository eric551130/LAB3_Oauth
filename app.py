from flask import Flask, request, redirect, url_for
from flask import render_template
import requests

app = Flask(__name__)

CLIENT_ID = 'YOUR CLINET ID'
CLIENT_SECRET = 'YOUR CLIENT SECRET'
result_list = []

@app.route("/")
def hello():
    return render_template('main.html')

@app.route("/oauthlab", methods=['GET'])
def login_demo():
    global CLIENT_ID
    global CLIENT_SECRET
    global result_list

    CODE = request.args.get('code')
    print(CODE)

    ### POST 取得TOKEN
    data = {
        'client_id' : CLIENT_ID,
        'client_secret' : CLIENT_SECRET,
        'code' : CODE,
    }
    header = {'Accept': 'application/json'}
    r = requests.post('https://github.com/login/oauth/access_token', data=data, headers=header)
    r_js = r.json()
    print(r_js['access_token'])
    token = r_js['access_token']

    ### GET 取得資料
    GET_header = {
        'Accept': 'application/json',
        'Authorization': f'token {token}'
    }
    Github_header = {
        'Accept': 'application/json',
        'Authorization': f'token {token}'
    }
    result = requests.get('https://api.github.com/user', headers=GET_header)
    result_user = result.json()
    result_list.append(result_user)

    result2 = requests.get(f'https://api.github.com/user/repos', headers=Github_header)
    #print(result2.url)
    result_repos = result2.json()

    repo_list = []
    for result_repo in result_repos:
        repo_list.append(result_repo['name'])
    result_list.append(repo_list)

    return redirect(url_for('welcome'))
@app.route("/users")
def welcome():
    global result_list

    return render_template('hello.html', data=result_list)


if __name__ == '__main__':
    #app.debug = True
    app.run()