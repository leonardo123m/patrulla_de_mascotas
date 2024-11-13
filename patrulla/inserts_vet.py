import flask
import pymysql

inserts = flask.Blueprint('inserts', __name__)

def insertar_veterinarias():
    # Datos manuales a insertar
    veterinarias_data = [
        ('México', 'CDMX', 'Veterinaria A', 'Cerca del parque X', '8:00 - 18:00', 'Av. Reforma', 100, '555-1234', 'Colonia 1', '01000', '19.432608', '-99.133209', 'imagen1.jpg', 'imagen2.jpg', 'imagen3.jpg'),
        ('México', 'Jalisco', 'Veterinaria B', 'Frente a la plaza Y', '9:00 - 20:00', 'Calle Futura', 200, '555-5678', 'Colonia 2', '01234', '20.659699', '-103.349609', 'imagen1.jpg', 'imagen2.jpg', 'imagen3.jpg'),
        ('México', 'Monterrey', 'Veterinaria C', 'Cerca del hospital Z', '10:00 - 19:00', 'Calle Principal', 300, '555-8765', 'Colonia 3', '01500', '25.671081', '-100.309418', 'imagen1.jpg', 'imagen2.jpg', 'imagen3.jpg'),
    ]
    
    # Conexion a la base de datos
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='patrulla')
    cursor = conn.cursor()

    # Consulta para insertar los datos si no existen
    query_check = """
    SELECT COUNT(*) FROM veterinarias 
    WHERE latitud = %s AND longitud = %s
    """
    
    query_insert = """
    INSERT INTO veterinarias (pais, estado, nombre_vet, referencia, horario, calle_avenida, numero_calle, telefono, 
                              colonia, codigo_postal, latitud, longitud, imagen1, imagen2, imagen3)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    for data in veterinarias_data:
        # Verificar si ya existe un registro con las mismas coordenadas
        cursor.execute(query_check, (data[10], data[11]))  # latitud y longitud
        count = cursor.fetchone()[0]
        
        if count == 0:  # Si no existe, hacer el insert
            cursor.execute(query_insert, data)
            conn.commit()
    
    cursor.close()
    conn.close()
