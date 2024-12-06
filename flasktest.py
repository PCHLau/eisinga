from flask import Flask, render_template

from orbittest import plotter

app = Flask(__name__)

@app.route('/')
def home():
    plotter()
    return render_template('test.html')
if __name__ == '__main__':
    app.run(debug=True)