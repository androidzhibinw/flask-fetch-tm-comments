import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask import Flask,render_template,request
import fetch
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def hello_world():
    if request.method == 'POST':
        data = request.form
        url = data['url']
        try:
            comments = fetch.getComments(url,bad=True)
        except Error as e:
            comments =e 
        return render_template('home.html',comments=comments,url=url)
    else:
        return render_template('home.html',comments=None,url=None)

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)

