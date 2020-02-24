import twitter
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            twitter.main(request.form['name'])
            return redirect(url_for('map'))
        except:
            return render_template('error.html')
    else:
        return render_template('index.html')


@app.route('/map', methods=['GET'])
def map():
    return render_template('friends.html')


if __name__ == '__main__':
    app.run(debug=True)
