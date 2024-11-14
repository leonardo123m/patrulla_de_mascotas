import flask
import pymysql

inserts = flask.Blueprint('inserts', __name__)

def insertar_veterinarias():
    # Datos manuales a insertar
    veterinarias_data = [
    ('México', 'Aguascalientes', 'Dog Paw', 
     'En la avenida donde se encuentra, en las dos esquinas de la calle hay tiendas (una de abarrotes y otro supermercado mini), casi en el centro de la calle',
     'Lunes: Aniversario del Inicio de la Revolución Mexicana (feriado), 8 a.m.–11 p.m. (horarios pueden variar)',
     'Martes: 8 a.m.–11 p.m.','Miércoles: 8 a.m.–11 p.m.','Jueves: 8 a.m.–11 p.m.','Viernes: 8 a.m.–11 p.m.','Sábado: 8 a.m.–11 p.m.',
     'Domingo: 8 a.m.–11 p.m.','Av. Gral. Mariano Escobedo',213, '449 977 6638', 'Casa Blanca', '20297',21.857064,-102.337144, 
     'https://fastly.4sqi.net/img/general/width960/72107241_ZOWfADXhNvxxmhmHkhra4ShgWUtNSlqiynoV5icojOU.jpg',
     'https://fastly.4sqi.net/img/general/width960/32419903_6IAPogdRoZB6blHnsJjaHbK6iwSfOAJd7Wk7fM6GT6Q.jpg',
     'https://fastly.4sqi.net/img/general/width960/4091625_Y8es5NsAIN0mWYfWzTkRmDMI7Czc2-VDYj3TEgNRCQA.jpg'
    ),
    ('México','Aguscalientes','Veterinaria', 'Cerca de Pepe s Burgers', 'lunes (Aniversario del Inicio de la Revolución Mexicana (feriado)), Abierto las 24 horas, Los horarios pueden variar',
     'martes, Abierto las 24 horas', 'miércoles, Abierto las 24 horas','jueves, Abierto las 24 horas','viernes, Abierto las 24 horas',
     'sábado, Abierto las 24 horas','domingo, Abierto las 24 horas','Av Heroe Inmortal', 810,'449 107 7233', 'Morelos I',
     '20298',21.8537292,-102.2701649,'https://w7.pngwing.com/pngs/609/906/png-transparent-engineering-design-process-engineering-design-process-business-design-text-vector-icons-engineering-thumbnail.png',
     'https://w7.pngwing.com/pngs/609/906/png-transparent-engineering-design-process-engineering-design-process-business-design-text-vector-icons-engineering-thumbnail.png',
     'https://w7.pngwing.com/pngs/609/906/png-transparent-engineering-design-process-engineering-design-process-business-design-text-vector-icons-engineering-thumbnail.png' )
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
    INSERT INTO veterinarias (pais, estado, nombre_vet, referencia, lunes, martes, miercoles, jueves, viernes,
      sabado, domingo,  calle_avenida, numero_calle, telefono, 
                              colonia, codigo_postal, latitud, longitud, imagen1, imagen2, imagen3)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for data in veterinarias_data:
        # Verificar si ya existe un registro con las mismas coordenadas
        cursor.execute(query_check, (data[16], data[17]))  # latitud y longitud
        count = cursor.fetchone()[0]
        
        if count == 0:  # Si no existe, hacer el insert
            cursor.execute(query_insert, data)
            conn.commit()

    
    cursor.close()
    conn.close()
