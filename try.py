from flask import Flask, send_from_directory, render_template, request, redirect, url_for
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
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Ottenere il valore di ricerca
    search_value = request.form['search_value']
    order = request.form.get('ordering')

    # Connessione al database
    cursor = mysql.connection.cursor()

    # Eseguire la query di ricerca
    cursor.execute("SELECT id FROM products WHERE name LIKE %s", (search_value + '%',))

    # Ottenere i risultati
    results = cursor.fetchall()

    # Se sono stati trovati risultati
    print("stampo results", results)
    if results:
        # Restituire l'ID del primo risultato
        if order:
            cursor.execute("DELETE FROM products WHERE id = %s", [results[0][0]])
            mysql.connection.commit()
            cursor.close()
            return render_template('notfound.html')
        return redirect(url_for('product', product_id=results[0][0]))
    cursor.close()
    return render_template('notfound.html')

@app.route('/show_products')
def show_products():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from products')
    results = cursor.fetchall()
    return render_template('show_products.html', products=results)

@app.route('/product/<int:product_id>')
def product(product_id):
    # Connessione al database
    cursor = mysql.connection.cursor()

    # Eseguire la query per ottenere i dettagli del prodotto
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))

    # Ottenere i dettagli del prodotto
    product = cursor.fetchone()

    # Chiudere il cursore
    cursor.close()
    # Mostrare la pagina del prodotto
    return render_template('product.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)