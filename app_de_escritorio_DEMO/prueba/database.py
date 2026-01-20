"""
database.py
Sistema de base de datos SQLite para la aplicación SCORE2
Manejo de pacientes y cálculos de riesgo cardiovascular
"""

import sqlite3
from datetime import datetime
import json
import os


class DatabaseManager:
    """Gestor de base de datos SQLite para pacientes y cálculos"""

    def __init__(self, db_name='score2_pacientes.db'):
        """
        Inicializa el gestor de base de datos.

        Args:
            db_name (str): Nombre del archivo de base de datos
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.conectar()
        self.crear_tablas()

    def conectar(self):
        """Establece conexión con la base de datos"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            # Habilitar claves foráneas
            self.cursor.execute("PRAGMA foreign_keys = ON")
            return True
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return False

    def desconectar(self):
        """Cierra la conexión con la base de datos"""
        if self.conn:
            self.conn.close()

    def crear_tablas(self):
        """Crea las tablas necesarias si no existen"""
        try:
            # Tabla de pacientes
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS pacientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    dni TEXT UNIQUE,
                    fecha_nacimiento DATE,
                    sexo TEXT NOT NULL CHECK(sexo IN ('varon', 'mujer')),
                    telefono TEXT,
                    email TEXT,
                    direccion TEXT,
                    obra_social TEXT,
                    numero_afiliado TEXT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    activo BOOLEAN DEFAULT 1,
                    observaciones TEXT
                )
            ''')

            # Tabla de cálculos de riesgo
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS calculos_riesgo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    paciente_id INTEGER NOT NULL,
                    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    edad INTEGER NOT NULL,
                    fumador BOOLEAN NOT NULL,
                    pas INTEGER NOT NULL,
                    colesterol_no_hdl REAL NOT NULL,
                    region TEXT NOT NULL CHECK(region IN ('moderado', 'muy_alto')),
                    riesgo_porcentaje INTEGER NOT NULL,
                    categoria TEXT NOT NULL,
                    score_type TEXT NOT NULL,
                    peso REAL,
                    altura REAL,
                    imc REAL,
                    colesterol_total REAL,
                    hdl REAL,
                    ldl REAL,
                    trigliceridos REAL,
                    glucemia REAL,
                    hba1c REAL,
                    pad INTEGER,
                    frecuencia_cardiaca INTEGER,
                    perimetro_cintura REAL,
                    antecedentes_familiares TEXT,
                    medicacion_actual TEXT,
                    observaciones TEXT,
                    FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE
                )
            ''')

            # Tabla de seguimiento
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS seguimiento (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    paciente_id INTEGER NOT NULL,
                    fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    motivo TEXT,
                    diagnostico TEXT,
                    tratamiento TEXT,
                    proxima_cita DATE,
                    observaciones TEXT,
                    FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE
                )
            ''')

            # Tabla de usuarios (para control de acceso)
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE NOT NULL,
                    nombre_completo TEXT NOT NULL,
                    email TEXT,
                    rol TEXT CHECK(rol IN ('admin', 'medico', 'enfermera', 'administrativo')),
                    activo BOOLEAN DEFAULT 1,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al crear tablas: {e}")
            return False

    # ========================================================================
    # MÉTODOS PARA PACIENTES
    # ========================================================================

    def agregar_paciente(self, datos_paciente):
        """
        Agrega un nuevo paciente a la base de datos.

        Args:
            datos_paciente (dict): Diccionario con los datos del paciente

        Returns:
            int: ID del paciente creado o None si hay error
        """
        try:
            self.cursor.execute('''
                INSERT INTO pacientes 
                (nombre, apellido, dni, fecha_nacimiento, sexo, telefono, 
                 email, direccion, obra_social, numero_afiliado, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos_paciente.get('nombre'),
                datos_paciente.get('apellido'),
                datos_paciente.get('dni'),
                datos_paciente.get('fecha_nacimiento'),
                datos_paciente.get('sexo'),
                datos_paciente.get('telefono'),
                datos_paciente.get('email'),
                datos_paciente.get('direccion'),
                datos_paciente.get('obra_social'),
                datos_paciente.get('numero_afiliado'),
                datos_paciente.get('observaciones')
            ))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al agregar paciente: {e}")
            return None

    def obtener_paciente(self, paciente_id):
        """Obtiene los datos de un paciente por ID"""
        try:
            self.cursor.execute('SELECT * FROM pacientes WHERE id = ?', (paciente_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener paciente: {e}")
            return None

    def buscar_pacientes(self, criterio='', valor=''):
        """
        Busca pacientes por diferentes criterios.

        Args:
            criterio (str): 'nombre', 'dni', 'apellido', etc.
            valor (str): Valor a buscar

        Returns:
            list: Lista de pacientes encontrados
        """
        try:
            if criterio == 'nombre':
                self.cursor.execute('''
                    SELECT * FROM pacientes 
                    WHERE nombre LIKE ? OR apellido LIKE ?
                    AND activo = 1
                    ORDER BY apellido, nombre
                ''', (f'%{valor}%', f'%{valor}%'))
            elif criterio == 'dni':
                self.cursor.execute('''
                    SELECT * FROM pacientes 
                    WHERE dni LIKE ?
                    AND activo = 1
                ''', (f'%{valor}%',))
            else:
                self.cursor.execute('''
                    SELECT * FROM pacientes 
                    WHERE activo = 1
                    ORDER BY apellido, nombre
                ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al buscar pacientes: {e}")
            return []

    def actualizar_paciente(self, paciente_id, datos_paciente):
        """Actualiza los datos de un paciente"""
        try:
            self.cursor.execute('''
                UPDATE pacientes SET
                nombre = ?, apellido = ?, dni = ?, fecha_nacimiento = ?,
                sexo = ?, telefono = ?, email = ?, direccion = ?,
                obra_social = ?, numero_afiliado = ?, observaciones = ?
                WHERE id = ?
            ''', (
                datos_paciente.get('nombre'),
                datos_paciente.get('apellido'),
                datos_paciente.get('dni'),
                datos_paciente.get('fecha_nacimiento'),
                datos_paciente.get('sexo'),
                datos_paciente.get('telefono'),
                datos_paciente.get('email'),
                datos_paciente.get('direccion'),
                datos_paciente.get('obra_social'),
                datos_paciente.get('numero_afiliado'),
                datos_paciente.get('observaciones'),
                paciente_id
            ))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al actualizar paciente: {e}")
            return False

    def eliminar_paciente(self, paciente_id, soft_delete=True):
        """
        Elimina un paciente (lógico o físico).

        Args:
            paciente_id (int): ID del paciente
            soft_delete (bool): Si True, solo marca como inactivo
        """
        try:
            if soft_delete:
                self.cursor.execute(
                    'UPDATE pacientes SET activo = 0 WHERE id = ?',
                    (paciente_id,)
                )
            else:
                self.cursor.execute('DELETE FROM pacientes WHERE id = ?', (paciente_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al eliminar paciente: {e}")
            return False

    # ========================================================================
    # MÉTODOS PARA CÁLCULOS DE RIESGO
    # ========================================================================

    def agregar_calculo(self, datos_calculo):
        """Agrega un nuevo cálculo de riesgo"""
        try:
            self.cursor.execute('''
                INSERT INTO calculos_riesgo 
                (paciente_id, edad, fumador, pas, colesterol_no_hdl, region,
                 riesgo_porcentaje, categoria, score_type, peso, altura, imc,
                 colesterol_total, hdl, ldl, trigliceridos, glucemia, hba1c,
                 pad, frecuencia_cardiaca, perimetro_cintura,
                 antecedentes_familiares, medicacion_actual, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos_calculo.get('paciente_id'),
                datos_calculo.get('edad'),
                datos_calculo.get('fumador'),
                datos_calculo.get('pas'),
                datos_calculo.get('colesterol_no_hdl'),
                datos_calculo.get('region', 'moderado'),
                datos_calculo.get('riesgo_porcentaje'),
                datos_calculo.get('categoria'),
                datos_calculo.get('score_type'),
                datos_calculo.get('peso'),
                datos_calculo.get('altura'),
                datos_calculo.get('imc'),
                datos_calculo.get('colesterol_total'),
                datos_calculo.get('hdl'),
                datos_calculo.get('ldl'),
                datos_calculo.get('trigliceridos'),
                datos_calculo.get('glucemia'),
                datos_calculo.get('hba1c'),
                datos_calculo.get('pad'),
                datos_calculo.get('frecuencia_cardiaca'),
                datos_calculo.get('perimetro_cintura'),
                datos_calculo.get('antecedentes_familiares'),
                datos_calculo.get('medicacion_actual'),
                datos_calculo.get('observaciones')
            ))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al agregar cálculo: {e}")
            return None

    def obtener_calculos_paciente(self, paciente_id, limite=None):
        """Obtiene los cálculos de un paciente ordenados por fecha"""
        try:
            if limite:
                self.cursor.execute('''
                    SELECT * FROM calculos_riesgo 
                    WHERE paciente_id = ?
                    ORDER BY fecha_calculo DESC
                    LIMIT ?
                ''', (paciente_id, limite))
            else:
                self.cursor.execute('''
                    SELECT * FROM calculos_riesgo 
                    WHERE paciente_id = ?
                    ORDER BY fecha_calculo DESC
                ''', (paciente_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener cálculos: {e}")
            return []

    def obtener_estadisticas(self, fecha_inicio=None, fecha_fin=None):
        """Obtiene estadísticas generales de los cálculos"""
        try:
            query = '''
                SELECT 
                    COUNT(DISTINCT paciente_id) as total_pacientes,
                    COUNT(*) as total_calculos,
                    AVG(riesgo_porcentaje) as riesgo_promedio,
                    SUM(CASE WHEN categoria = 'Bajo' THEN 1 ELSE 0 END) as riesgo_bajo,
                    SUM(CASE WHEN categoria = 'Moderado' THEN 1 ELSE 0 END) as riesgo_moderado,
                    SUM(CASE WHEN categoria = 'Alto' THEN 1 ELSE 0 END) as riesgo_alto,
                    SUM(CASE WHEN fumador = 1 THEN 1 ELSE 0 END) as fumadores
                FROM calculos_riesgo
            '''

            if fecha_inicio and fecha_fin:
                query += ' WHERE fecha_calculo BETWEEN ? AND ?'
                self.cursor.execute(query, (fecha_inicio, fecha_fin))
            else:
                self.cursor.execute(query)

            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener estadísticas: {e}")
            return None

    # ========================================================================
    # MÉTODOS PARA EXPORTACIÓN
    # ========================================================================

    def exportar_a_csv(self, nombre_archivo='pacientes_export.csv'):
        """Exporta todos los pacientes y cálculos a CSV"""
        try:
            import csv

            # Exportar pacientes
            self.cursor.execute('''
                SELECT p.*, c.fecha_calculo, c.riesgo_porcentaje, c.categoria
                FROM pacientes p
                LEFT JOIN calculos_riesgo c ON p.id = c.paciente_id
                WHERE p.activo = 1
                ORDER BY p.apellido, p.nombre, c.fecha_calculo DESC
            ''')

            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([desc[0] for desc in self.cursor.description])
                writer.writerows(self.cursor.fetchall())

            return True
        except Exception as e:
            print(f"Error al exportar CSV: {e}")
            return False

    def backup_database(self, directorio='backups'):
        """Crea un backup de la base de datos"""
        try:
            if not os.path.exists(directorio):
                os.makedirs(directorio)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"{directorio}/backup_{timestamp}.db"

            backup_conn = sqlite3.connect(backup_name)
            self.conn.backup(backup_conn)
            backup_conn.close()

            return backup_name
        except Exception as e:
            print(f"Error al crear backup: {e}")
            return None


# ============================================================================
# EJEMPLO DE USO
# ============================================================================
if __name__ == "__main__":
    # Crear instancia del gestor
    db = DatabaseManager()

    # Agregar un paciente de ejemplo
    paciente_datos = {
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'dni': '12345678',
        'fecha_nacimiento': '1970-05-15',
        'sexo': 'varon',
        'telefono': '3794-123456',
        'email': 'juan.perez@email.com',
        'direccion': 'Av. Libertad 123, Corrientes',
        'obra_social': 'OSDE',
        'numero_afiliado': '001-123456-7',
        'observaciones': 'Paciente derivado de guardia'
    }

    paciente_id = db.agregar_paciente(paciente_datos)
    print(f"Paciente agregado con ID: {paciente_id}")

    # Agregar un cálculo de riesgo
    calculo_datos = {
        'paciente_id': paciente_id,
        'edad': 54,
        'fumador': True,
        'pas': 145,
        'colesterol_no_hdl': 5.2,
        'region': 'moderado',
        'riesgo_porcentaje': 28,
        'categoria': 'Alto',
        'score_type': 'SCORE2',
        'peso': 82.5,
        'altura': 1.75,
        'imc': 26.9
    }

    calculo_id = db.agregar_calculo(calculo_datos)
    print(f"Cálculo agregado con ID: {calculo_id}")

    # Obtener estadísticas
    stats = db.obtener_estadisticas()
    print(f"Estadísticas: {stats}")

    # Cerrar conexión
    db.desconectar()