from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'nomina'

mysql = MySQL(app)

@app.route('/Empleados')
def Empleados():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    data = cur.fetchall()
    cur.close()

    return render_template('empleados.html', usuarios=data)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', usuarios=data)



@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Datos insertados exitosamente")
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        cargo = request.form['cargo']
        telefono = request.form['telefono']
        email = request.form['email']
        salario = request.form['salario']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (nombre, cedula, cargo, telefono, email, salario) VALUES (%s, %s, %s, %s, %s, %s)", (nombre, cedula, cargo, telefono, email, salario))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("El empleado se ha eliminado correctamente")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuarios WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Empleados'))



@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        cargo = request.form['cargo']
        telefono = request.form['telefono']
        email = request.form['email']
        salario = request.form['salario']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE usuarios SET nombre=%s, cedula=%s, cargo=%s, telefono=%s, email=%s, salario=%s
        WHERE id=%s
        """, (nombre, cedula, cargo, telefono, email, salario, id_data))
        flash("Datos actualizados exitosamente")
        return redirect(url_for('Empleados'))




if __name__ == "__main__":
    app.run(debug=True)
