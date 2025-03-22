from flask import Flask, jsonify
from flask_mysqldb import MySQL

from config import config

app = Flask(__name__)

conexion=MySQL(app)


@app.route('/cursos', methods=['GET'])
def listar_cursos():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT codigo, nombre, creditos FROM curso"      
        cursor.execute(sql)  
        datos=cursor.fetchall()
        cursos=[]
        for fila in datos:
            curso={'codigo':fila[0],'nombre':fila[1],'creditos':fila[2]}
            cursos.append(curso)
        return jsonify({'cursos':cursos,'mensaje':"Cursos listados."})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

@app.route('/cursos/<codigo>', methods=['GET'])
def leer_curso(codigo):
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT codigo, nombre, creditos FROM curso Where codigo = '{0}'" .format(codigo)    
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            curso={'codigo':datos[0],'nombre':datos[1],'creditos':datos[2]}
            return jsonify({'curso':curso,'mensaje':"Curso encontrado."})
        else:
            return jsonify({'mensaje':"Curso no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

def pagina_no_encontrada(error):
    return""" 
    <html>
        <head>
            <style>
                h1 {
                    color: blue;
                }
                p {
                    font-size: 18px;
                    color: #333;
                }
            </style>
        </head>
        <body>
            <h1>Error 404 - Página No Encontrada</h1>,404
            <p>Lo sentimos, la página que estás buscando no existe o ha sido movida.  
            Verifica la URL e intenta nuevamente.</p>
        </body>
    </html>
    """, 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontrada)
    app.run()