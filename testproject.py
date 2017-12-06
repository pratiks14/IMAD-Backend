from flask import Flask, render_template, request, make_response, redirect, url_for
import httplib2
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
	return "Hello World-Pratik shetty"

@app.route('/authors')
def authors():
	h = httplib2.Http()
	url_aut = "https://jsonplaceholder.typicode.com/users"
	url_post = "https://jsonplaceholder.typicode.com/posts"
	response = h.request(url_aut,'GET')[1]
	response = json.loads(response)
	response2 = h.request(url_post,'GET')[1]
	response2 = json.loads(response2)
	post_num = {}

	for j in range(len(response2)):
		user_id = response2[j].get("userId")
		if post_num.get(user_id) is None:
			post_num[user_id]=1
		else:
			post_num[user_id]+=1

	output = '<h3>Authors</h3><ul>'

	for i in  range(len(response)):
		output += '<li><b>'
		output += response[i].get("name")
		output += '</b> has posted '
		output +=  str(post_num[response[i].get("id")]) + " times."
		output +='</li>'
	output += '</ul>'
	return output

@app.route('/setcookie')
def set_cookie():
	response = make_response(redirect('/'))
	response.set_cookie('name',value="pratik shetty")
	response.set_cookie('age',value="23")
	return response

@app.route('/getcookie')
def get_cookie():
	name = request.cookies.get('name')
	age = request.cookies.get('age')
	output = '<h4>Name : '
	output += name + '</h4>'
	output += '<h4>Age :'
	output += age + '</h4>'
	return output


@app.route('/robots.txt')
def deny_req():
	url = "http://httpbin.org/deny"
	h = httplib2.Http()
	resp =  make_response(h.request(url,'GET')[1],401)
	resp.headers['content-type'] = 'text/plain'
	return resp

@app.route('/input',methods=['GET','POST'])
def input_form():
	if request.method == 'POST':
		name = request.form.get('name')
		print "Name : "+ name
		return redirect(url_for('input_form'))
	else:
		return render_template('input.html')

@app.route('/image')
def ret_image():
	return make_response(url_for('static',filename='creepy.jpg'))

if __name__ == '__main__':
    app.secret_key = "secretkey"
    app.debug = True
    app.run(host='0.0.0.0', port=8080)