from flask import Flask, render_template

app = Flask(__name__)

@app.route('home') # This is the Home page
def index():
    return render_template('home.html')

@app.route('/about') # This is the About page
def about():
    return render_template('about.html')

@app.route('/contact') # This is the Contact page
def contact():
    return render_template('contact.html')

@app.route('/DOM')
def index():
    return render_template('DOM.html')

if __name__ == '__main__':
    app.run(debug=True)