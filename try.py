from flask import Flask, send_from_directory, render_template
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

@app.route('/')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT user, host FROM mysql.user''')
    rv = cur.fetchall()
    return str(rv)
@app.route('/products')
def list_products():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM products''')
    rv = cur.fetchall()
    return str(rv)

@app.route('/static')
def static_try():
    return send_from_directory('statics' ,'index_static.html')

@app.route('/renderer')
def render_try():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM products''')
    products = cur.fetchall()
    print(products)
    return(render_template('index_renderer.html', products=products))
if __name__ == '__main__':
    app.run(debug=True)