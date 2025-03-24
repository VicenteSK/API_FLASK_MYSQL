from flask import Flask, jsonify, request
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
@app.route('/cursos', methods=['POST'])
def registrar_curso():
    try:
        cursor = conexion.connection.cursor()

        # Verificar si el código ya existe
        sql_verificar = "SELECT codigo FROM curso WHERE codigo = %s"
        cursor.execute(sql_verificar, (request.json['codigo'],))
        existe = cursor.fetchone()

        if existe:
            return jsonify({'mensaje': "No se puede ingresar, código duplicado"}), 400  # Respuesta con error 400

        # Si no existe, insertar el nuevo curso
        sql_insertar = "INSERT INTO curso (codigo, nombre, creditos) VALUES (%s, %s, %s)"
        valores = (request.json['codigo'], request.json['nombre'], request.json['creditos'])
        cursor.execute(sql_insertar, valores)
        conexion.connection.commit()

        return jsonify({'mensaje': "Curso registrado correctamente"}), 201  # Código 201 para creación exitosa
    except Exception as ex:
        return jsonify({'mensaje': "Error en el servidor"}), 500
    
@app.route('/cursos/<codigo>', methods=['PUT'])
def actualizar_curso(codigo):    
    try:
        cursor = conexion.connection.cursor()

        # Verificar si el curso existe antes de actualizarlo
        sql_verificar = "SELECT codigo FROM curso WHERE codigo = %s"
        cursor.execute(sql_verificar, (codigo,))
        existe = cursor.fetchone()

        if not existe:
            return jsonify({'mensaje': "No se puede actualizar, código no encontrado"}), 404  # Respuesta con error 404

        # Si el curso existe, proceder con la actualización
        sql_actualizar = """UPDATE curso 
                            SET nombre = %s, creditos = %s 
                            WHERE codigo = %s"""
        valores = (request.json['nombre'], request.json['creditos'], codigo)

        cursor.execute(sql_actualizar, valores)
        conexion.connection.commit()

        return jsonify({'mensaje': "Curso actualizado correctamente"}), 200  # Código 200 para éxito
    except Exception as ex:
        return jsonify({'mensaje': "Error en el servidor"}), 500


@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    try:
        cursor = conexion.connection.cursor()

        # Verificar si el curso existe
        sql_verificar = "SELECT codigo FROM curso WHERE codigo = %s"
        cursor.execute(sql_verificar, (codigo,))
        existe = cursor.fetchone()

        if not existe:
            return jsonify({'mensaje': "Código de curso no encontrado"}), 404  # Código 404 si no existe

        # Si existe, proceder con la eliminación
        sql_eliminar = "DELETE FROM curso WHERE codigo = %s"
        cursor.execute(sql_eliminar, (codigo,))
        conexion.connection.commit()  # Confirmar eliminación

        return jsonify({'mensaje': "Curso eliminado correctamente"}), 200  # Código 200 para éxito
    except Exception as ex:
        return jsonify({'mensaje': "Error en el servidor"}), 500


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