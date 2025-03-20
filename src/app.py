from flask import Flask
from flask_mysqldb import MySQL

from config import config

app = Flask(__name__)

conexion=MySQL(app)


@app.route('/cursos')
def listar_cursos():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT codigo, nombre, creditos FROM curso"      
        cursor.execute(sql)  
        datos=cursor.fetchall()
        print(datos)
        return"Cursos listados"
    except Exception as ex:
        return "Error"


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
            <h1>Error 404 - Página No Disponible</h1>
            <p>Lo sentimos, la página que estás buscando no existe o ha sido movida.  
            Verifica la URL e intenta nuevamente.</p>
        </body>
    </html>
    """, 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontrada)
    app.run()