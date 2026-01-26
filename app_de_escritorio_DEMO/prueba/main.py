"""
main.py
Aplicación de escritorio para cálculo de riesgo cardiovascular SCORE2/SCORE2-OP
Unidad de Prevención Cardiometabólica - Corrientes Capital
MODIFICADO: Colesterol únicamente en mg/dl
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date

# Importar matplotlib solo si está disponible
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    MATPLOTLIB_DISPONIBLE = True
except ImportError:
    MATPLOTLIB_DISPONIBLE = False
    print("Matplotlib no disponible. Las funciones de gráficos estarán limitadas.")

from database import DatabaseManager
from tablas_score2 import calcular_riesgo

class SCORE2App:
    """Aplicación principal para cálculo de riesgo cardiovascular"""

    def __init__(self, root):
        self.root = root
        self.root.title("SCORE2 - Calculadora de Riesgo Cardiovascular | ISSUNNE Corrientes")
        self.root.geometry("1400x900")
        self.root.state('zoomed')  # Maximizar ventana

        # Estilos
        self.configurar_estilos()

        # Base de datos
        self.db = DatabaseManager()

        # Variables
        self.paciente_actual = None
        self.calculos_actuales = []

        # Crear interfaz
        self.crear_menu()
        self.crear_interfaz()

        # Cargar datos iniciales
        self.actualizar_lista_pacientes()

    def configurar_estilos(self):
        """Configura los estilos de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')

        # Colores
        self.color_primario = '#2563eb'
        self.color_secundario = '#1e40af'
        self.color_exito = '#10b981'
        self.color_advertencia = '#f59e0b'
        self.color_peligro = '#ef4444'
        self.color_fondo = '#f8fafc'

        # Estilos personalizados
        style.configure('Header.TLabel',
                       font=('Segoe UI', 16, 'bold'),
                       foreground=self.color_primario)

        style.configure('Subheader.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=self.color_secundario)

        style.configure('Primary.TButton',
                       font=('Segoe UI', 10),
                       background=self.color_primario,
                       foreground='white')

        style.configure('Success.TButton',
                       font=('Segoe UI', 10),
                       background=self.color_exito)

    def crear_menu(self):
        """Crea el menú principal"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menú Archivo
        archivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Nuevo Paciente", command=self.mostrar_nuevo_paciente)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Exportar a CSV", command=self.exportar_csv)
        archivo_menu.add_command(label="Backup Base de Datos", command=self.crear_backup)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.root.quit)

        # Menú Pacientes
        pacientes_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Pacientes", menu=pacientes_menu)
        pacientes_menu.add_command(label="Buscar Paciente", command=self.buscar_paciente)
        pacientes_menu.add_command(label="Lista de Pacientes", command=self.mostrar_lista_pacientes)

        # Menú Estadísticas
        stats_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Estadísticas", menu=stats_menu)
        stats_menu.add_command(label="Dashboard", command=self.mostrar_estadisticas)
        stats_menu.add_command(label="Gráficos", command=self.mostrar_graficos)

        # Menú Ayuda
        ayuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu)
        ayuda_menu.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        ayuda_menu.add_command(label="Guía de uso", command=self.mostrar_guia)

    def crear_interfaz(self):
        """Crea la interfaz principal con pestañas"""
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Pestaña 1: Calculadora
        self.tab_calculadora = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_calculadora, text='  📊 Calculadora  ')
        self.crear_tab_calculadora()

        # Pestaña 2: Pacientes
        self.tab_pacientes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_pacientes, text='  👥 Pacientes  ')
        self.crear_tab_pacientes()

        # Pestaña 3: Historial
        self.tab_historial = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_historial, text='  📋 Historial  ')
        self.crear_tab_historial()

        # Pestaña 4: Estadísticas
        self.tab_estadisticas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_estadisticas, text='  📈 Estadísticas  ')
        self.crear_tab_estadisticas()

        # Barra de estado
        self.crear_barra_estado()

    def crear_tab_calculadora(self):
        """Crea la pestaña de calculadora de riesgo"""
        # Frame principal con dos columnas y scroll
        canvas = tk.Canvas(self.tab_calculadora)
        scrollbar = ttk.Scrollbar(self.tab_calculadora, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame principal dentro del scrollable
        main_frame = ttk.Frame(scrollable_frame)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Columna izquierda: Formulario
        left_frame = ttk.LabelFrame(main_frame, text="Datos del Paciente", padding=20)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

        # Selección de paciente
        ttk.Label(left_frame, text="Paciente:", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=0, sticky='w', pady=5)

        paciente_frame = ttk.Frame(left_frame)
        paciente_frame.grid(row=0, column=1, sticky='ew', pady=5)

        self.var_paciente = tk.StringVar()
        self.combo_paciente = ttk.Combobox(paciente_frame, textvariable=self.var_paciente,
                                           state='readonly', width=30)
        self.combo_paciente.pack(side='left', fill='x', expand=True)
        self.combo_paciente.bind('<<ComboboxSelected>>', self.on_paciente_seleccionado)

        ttk.Button(paciente_frame, text="Nuevo", command=self.mostrar_nuevo_paciente,
                  width=8).pack(side='left', padx=(5, 0))

        # Datos demográficos
        ttk.Separator(left_frame, orient='horizontal').grid(
            row=1, column=0, columnspan=2, sticky='ew', pady=10)

        row = 2

        # Fecha de nacimiento (como HeartScore)
        ttk.Label(left_frame, text="Fecha de Nacimiento *", foreground='red').grid(
            row=row, column=0, sticky='w', pady=5)

        fecha_frame = ttk.Frame(left_frame)
        fecha_frame.grid(row=row, column=1, sticky='w', pady=5)

        self.var_mes = tk.StringVar()
        self.var_anio = tk.StringVar()

        ttk.Entry(fecha_frame, textvariable=self.var_mes, width=8).pack(side='left')
        ttk.Label(fecha_frame, text="/").pack(side='left', padx=2)
        ttk.Entry(fecha_frame, textvariable=self.var_anio, width=10).pack(side='left')
        ttk.Label(fecha_frame, text="(Mes / Año)", foreground='gray',
                 font=('Segoe UI', 8)).pack(side='left', padx=(5, 0))
        row += 1

        # Sexo
        ttk.Label(left_frame, text="Sexo *", foreground='red').grid(
            row=row, column=0, sticky='w', pady=5)
        self.var_sexo = tk.StringVar(value='varon')
        sexo_frame = ttk.Frame(left_frame)
        sexo_frame.grid(row=row, column=1, sticky='w', pady=5)
        ttk.Radiobutton(sexo_frame, text="Hombre", variable=self.var_sexo,
                       value='varon').pack(side='left')
        ttk.Radiobutton(sexo_frame, text="Mujer", variable=self.var_sexo,
                       value='mujer').pack(side='left', padx=(10, 0))
        row += 1

        # Parámetros clínicos
        ttk.Separator(left_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky='ew', pady=10)
        row += 1

        # Presión Arterial Sistólica (PAS)
        ttk.Label(left_frame, text="Presión Arterial Sistólica *",
                 foreground='red').grid(row=row, column=0, sticky='w', pady=5)
        pas_frame = ttk.Frame(left_frame)
        pas_frame.grid(row=row, column=1, sticky='w', pady=5)
        self.var_pas = tk.StringVar()
        ttk.Entry(pas_frame, textvariable=self.var_pas, width=10).pack(side='left')
        ttk.Label(pas_frame, text="mmHg", foreground='gray').pack(side='left', padx=(5, 0))
        row += 1

        # Total Cholesterol - SOLO mg/dl
        ttk.Label(left_frame, text="Colesterol Total *",
                 foreground='red').grid(row=row, column=0, sticky='w', pady=5)
        col_total_frame = ttk.Frame(left_frame)
        col_total_frame.grid(row=row, column=1, sticky='w', pady=5)

        self.var_col_total = tk.StringVar()
        ttk.Entry(col_total_frame, textvariable=self.var_col_total, width=10).pack(side='left')
        ttk.Label(col_total_frame, text="mg/dl", foreground='gray').pack(side='left', padx=(5, 0))
        row += 1

        # HDL-Cholesterol - SOLO mg/dl
        ttk.Label(left_frame, text="Colesterol-HDL *",
                 foreground='red').grid(row=row, column=0, sticky='w', pady=5)
        hdl_frame = ttk.Frame(left_frame)
        hdl_frame.grid(row=row, column=1, sticky='w', pady=5)
        self.var_hdl = tk.StringVar()
        ttk.Entry(hdl_frame, textvariable=self.var_hdl, width=10).pack(side='left')
        ttk.Label(hdl_frame, text="mg/dl", foreground='gray').pack(side='left', padx=(5, 0))
        row += 1

        # LDL-Cholesterol (opcional) - SOLO mg/dl
        ttk.Label(left_frame, text="Colesterol-LDL",
                 foreground='gray').grid(row=row, column=0, sticky='w', pady=5)
        ldl_frame = ttk.Frame(left_frame)
        ldl_frame.grid(row=row, column=1, sticky='w', pady=5)
        self.var_ldl = tk.StringVar()
        ttk.Entry(ldl_frame, textvariable=self.var_ldl, width=10).pack(side='left')
        ttk.Label(ldl_frame, text="mg/dl", foreground='gray').pack(side='left', padx=(5, 0))
        row += 1

        # Current Smoker
        ttk.Label(left_frame, text="¿Fumador activo? *",
                 foreground='red').grid(row=row, column=0, sticky='w', pady=5)
        self.var_fumador = tk.BooleanVar()
        fumador_frame = ttk.Frame(left_frame)
        fumador_frame.grid(row=row, column=1, sticky='w', pady=5)
        ttk.Radiobutton(fumador_frame, text="Si", variable=self.var_fumador,
                       value=True).pack(side='left')
        ttk.Radiobutton(fumador_frame, text="No", variable=self.var_fumador,
                       value=False).pack(side='left', padx=(10, 0))
        row += 1

        # Región de riesgo
        ttk.Separator(left_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky='ew', pady=10)
        row += 1

        ttk.Label(left_frame, text="Región de Riesgo:", font=('Segoe UI', 10, 'bold')).grid(
            row=row, column=0, sticky='w', pady=5)
        self.var_region = tk.StringVar(value='moderado')  # MODERADO por defecto
        region_combo = ttk.Combobox(left_frame, textvariable=self.var_region,
                                   values=['moderado', 'muy_alto'],
                                   state='readonly', width=20)
        region_combo.grid(row=row, column=1, sticky='w', pady=5)
        row += 1

        # Nota sobre la región
        nota_region = tk.Frame(left_frame, bg='#fff3cd', relief=tk.RIDGE, borderwidth=1)
        nota_region.grid(row=row, column=0, columnspan=2, sticky='ew', pady=5, padx=5)

        tk.Label(nota_region,
                text="💡 Usar MODERADO para Argentina (según tablas ESC 2021)",
                bg='#fff3cd', font=('Segoe UI', 8, 'bold'),
                foreground='#856404').pack(anchor='w', padx=10, pady=5)
        row += 1

        # Nota informativa sobre no-HDL
        info_frame = tk.Frame(left_frame, bg='#e3f2fd', relief=tk.RIDGE, borderwidth=1)
        info_frame.grid(row=row, column=0, columnspan=2, sticky='ew', pady=10, padx=5)

        tk.Label(info_frame,
                text="ℹ️ El colesterol no-HDL se calcula automáticamente:",
                bg='#e3f2fd', font=('Segoe UI', 9, 'bold'),
                foreground='#1976d2').pack(anchor='w', padx=10, pady=(5, 0))
        tk.Label(info_frame,
                text="no-HDL = Total Cholesterol - HDL (en mg/dl)",
                bg='#e3f2fd', font=('Segoe UI', 8, 'italic'),
                foreground='#424242').pack(anchor='w', padx=20, pady=(0, 5))
        row += 1

        # Datos adicionales (opcionales)
        ttk.Separator(left_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky='ew', pady=10)
        row += 1

        ttk.Label(left_frame, text="Datos Adicionales (opcional)",
                 font=('Segoe UI', 9, 'italic'), foreground='gray').grid(
            row=row, column=0, columnspan=2, sticky='w', pady=5)
        row += 1

        # Peso, Altura
        datos_frame = ttk.Frame(left_frame)
        datos_frame.grid(row=row, column=0, columnspan=2, sticky='ew', pady=5)

        ttk.Label(datos_frame, text="Peso (kg):").pack(side='left')
        self.var_peso = tk.StringVar()
        ttk.Entry(datos_frame, textvariable=self.var_peso, width=8).pack(side='left', padx=5)

        ttk.Label(datos_frame, text="Altura (m):").pack(side='left', padx=(10, 0))
        self.var_altura = tk.StringVar()
        ttk.Entry(datos_frame, textvariable=self.var_altura, width=8).pack(side='left', padx=5)
        row += 1

        # Botón calcular
        ttk.Button(left_frame, text="📊 CALCULAR RIESGO",
                  command=self.calcular_riesgo_click,
                  style='Primary.TButton').grid(
            row=row, column=0, columnspan=2, sticky='ew', pady=20)
        row += 1

        # Botón guardar
        ttk.Button(left_frame, text="💾 GUARDAR CÁLCULO",
                  command=self.guardar_calculo,
                  style='Success.TButton').grid(
            row=row, column=0, columnspan=2, sticky='ew')
        row += 1

        # Recordatorio de campos requeridos
        ttk.Label(left_frame, text="* Campos requeridos / Required fields",
                 font=('Segoe UI', 8), foreground='red').grid(
            row=row, column=0, columnspan=2, sticky='w', pady=(10, 0))

        # Columna derecha: Resultados
        right_frame = ttk.LabelFrame(main_frame, text="Resultado del Cálculo", padding=20)
        right_frame.grid(row=0, column=1, sticky='nsew')

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Área de resultados
        self.resultado_frame = ttk.Frame(right_frame)
        self.resultado_frame.pack(fill='both', expand=True)

        # Mensaje inicial
        ttk.Label(self.resultado_frame,
                 text="Complete los datos y presione 'Calcular Riesgo'",
                 font=('Segoe UI', 12),
                 foreground='gray').pack(expand=True)

    def crear_tab_pacientes(self):
        """Crea la pestaña de gestión de pacientes"""
        # Frame de búsqueda
        search_frame = ttk.Frame(self.tab_pacientes)
        search_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(search_frame, text="Buscar:", font=('Segoe UI', 10)).pack(side='left')
        # self.var_buscar = tk.StringVar()
        # self.var_buscar.trace('w', lambda *args: self.actualizar_lista_pacientes())
        # ttk.Entry(search_frame, textvariable=self.var_buscar, width=30).pack(
        #     side='left', padx=10)
        self.var_buscar = tk.StringVar()
        self.var_buscar.trace_add('write', lambda *args: self.actualizar_lista_pacientes())
        ttk.Entry(search_frame, textvariable=self.var_buscar, width=30).pack(
            side='left', padx=10)

        ttk.Button(search_frame, text="➕ Nuevo Paciente",
                  command=self.mostrar_nuevo_paciente).pack(side='right')

        # Lista de pacientes
        list_frame = ttk.Frame(self.tab_pacientes)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Scrollbars
        scroll_y = ttk.Scrollbar(list_frame, orient='vertical')
        scroll_y.pack(side='right', fill='y')

        scroll_x = ttk.Scrollbar(list_frame, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')

        # Treeview
        self.tree_pacientes = ttk.Treeview(list_frame,
                                          columns=('id', 'apellido', 'nombre', 'dni',
                                                  'edad', 'sexo', 'telefono'),
                                          show='headings',
                                          yscrollcommand=scroll_y.set,
                                          xscrollcommand=scroll_x.set)

        scroll_y.config(command=self.tree_pacientes.yview)
        scroll_x.config(command=self.tree_pacientes.xview)

        # Configurar columnas
        self.tree_pacientes.heading('id', text='ID')
        self.tree_pacientes.heading('apellido', text='Apellido')
        self.tree_pacientes.heading('nombre', text='Nombre')
        self.tree_pacientes.heading('dni', text='DNI')
        self.tree_pacientes.heading('edad', text='Edad')
        self.tree_pacientes.heading('sexo', text='Sexo')
        self.tree_pacientes.heading('telefono', text='Teléfono')

        self.tree_pacientes.column('id', width=50)
        self.tree_pacientes.column('apellido', width=150)
        self.tree_pacientes.column('nombre', width=150)
        self.tree_pacientes.column('dni', width=100)
        self.tree_pacientes.column('edad', width=60)
        self.tree_pacientes.column('sexo', width=80)
        self.tree_pacientes.column('telefono', width=120)

        self.tree_pacientes.pack(fill='both', expand=True)

        # Botones de acción
        btn_frame = ttk.Frame(self.tab_pacientes)
        btn_frame.pack(fill='x', padx=20, pady=10)

        ttk.Button(btn_frame, text="Ver Detalles",
                  command=self.ver_paciente).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Editar",
                  command=self.editar_paciente).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📄 Exportar PDF",
                  command=self.exportar_paciente_pdf).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Eliminar",
                  command=self.eliminar_paciente).pack(side='left', padx=5)

    def crear_tab_historial(self):
        """Crea la pestaña de historial de cálculos"""
        # Frame principal
        frame_principal = ttk.Frame(self.tab_historial)
        frame_principal.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(frame_principal,
                 text="Historial de Cálculos",
                 style='Header.TLabel').pack(pady=(0, 20))

        # Botones de acción
        btn_frame = ttk.Frame(frame_principal)
        btn_frame.pack(fill='x', pady=(0, 10))

        ttk.Button(btn_frame, text="🔄 Actualizar",
                  command=self.cargar_historial).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📊 Exportar CSV",
                  command=self.exportar_csv).pack(side='left', padx=5)

        # Tabla de historial
        hist_frame = ttk.Frame(frame_principal)
        hist_frame.pack(fill='both', expand=True)

        # Scrollbars
        scroll_y = ttk.Scrollbar(hist_frame, orient='vertical')
        scroll_y.pack(side='right', fill='y')

        scroll_x = ttk.Scrollbar(hist_frame, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')

        self.tree_historial = ttk.Treeview(hist_frame,
                                          columns=('id', 'fecha', 'paciente', 'edad',
                                                  'fumador', 'pas', 'col_no_hdl',
                                                  'riesgo', 'categoria', 'score', 'region'),
                                          show='headings',
                                          yscrollcommand=scroll_y.set,
                                          xscrollcommand=scroll_x.set)

        scroll_y.config(command=self.tree_historial.yview)
        scroll_x.config(command=self.tree_historial.xview)

        # Configurar columnas
        self.tree_historial.heading('id', text='ID')
        self.tree_historial.heading('fecha', text='Fecha')
        self.tree_historial.heading('paciente', text='Paciente')
        self.tree_historial.heading('edad', text='Edad')
        self.tree_historial.heading('fumador', text='Fumador')
        self.tree_historial.heading('pas', text='PAS')
        self.tree_historial.heading('col_no_hdl', text='no-HDL')
        self.tree_historial.heading('riesgo', text='Riesgo %')
        self.tree_historial.heading('categoria', text='Categoría')
        self.tree_historial.heading('score', text='Tipo')
        self.tree_historial.heading('region', text='Región')

        # Anchos de columnas
        self.tree_historial.column('id', width=50)
        self.tree_historial.column('fecha', width=150)
        self.tree_historial.column('paciente', width=200)
        self.tree_historial.column('edad', width=60)
        self.tree_historial.column('fumador', width=70)
        self.tree_historial.column('pas', width=60)
        self.tree_historial.column('col_no_hdl', width=80)
        self.tree_historial.column('riesgo', width=80)
        self.tree_historial.column('categoria', width=100)
        self.tree_historial.column('score', width=80)
        self.tree_historial.column('region', width=100)

        self.tree_historial.pack(fill='both', expand=True)

        # Cargar datos iniciales
        self.cargar_historial()

    def cargar_historial(self):
        """Carga todos los cálculos en el historial"""
        # Limpiar tabla
        for item in self.tree_historial.get_children():
            self.tree_historial.delete(item)

        try:
            # Obtener todos los cálculos con datos de pacientes
            self.db.cursor.execute('''
                SELECT c.id, c.fecha_calculo, p.nombre, p.apellido, c.edad,
                       c.fumador, c.pas, c.colesterol_no_hdl, c.riesgo_porcentaje,
                       c.categoria, c.score_type, c.region
                FROM calculos_riesgo c
                JOIN pacientes p ON c.paciente_id = p.id
                WHERE p.activo = 1
                ORDER BY c.fecha_calculo DESC
            ''')

            calculos = self.db.cursor.fetchall()

            for calc in calculos:
                fumador_texto = 'Sí' if calc[5] else 'No'
                nombre_completo = f"{calc[3]}, {calc[2]}"  # Apellido, Nombre

                self.tree_historial.insert('', 'end', values=(
                    calc[0],  # id
                    calc[1],  # fecha
                    nombre_completo,  # paciente
                    calc[4],  # edad
                    fumador_texto,  # fumador
                    calc[6],  # pas
                    f"{calc[7]:.2f}" if calc[7] else '',  # col_no_hdl
                    f"{calc[8]}%",  # riesgo
                    calc[9],  # categoria
                    calc[10],  # score_type
                    calc[11]  # region
                ))
        except Exception as e:
            print(f"Error al cargar historial: {e}")
            import traceback
            traceback.print_exc()

    def crear_tab_estadisticas(self):
        """Crea la pestaña de estadísticas"""
        ttk.Label(self.tab_estadisticas,
                 text="Dashboard Estadístico",
                 style='Header.TLabel').pack(pady=20)

        # Frame de métricas
        metrics_frame = ttk.Frame(self.tab_estadisticas)
        metrics_frame.pack(fill='x', padx=20, pady=10)

        # Crear cards de métricas
        self.cards_frame = ttk.Frame(metrics_frame)
        self.cards_frame.pack(fill='x')

        # Botón actualizar
        ttk.Button(self.tab_estadisticas, text="🔄 Actualizar Estadísticas",
                  command=self.actualizar_estadisticas).pack(pady=10)

    def crear_barra_estado(self):
        """Crea la barra de estado en la parte inferior"""
        self.status_bar = ttk.Label(self.root, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Reloj
        self.actualizar_reloj()

    def actualizar_reloj(self):
        """Actualiza el reloj en la barra de estado"""
        ahora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.status_bar.config(text=f"Listo | {ahora}")
        self.root.after(1000, self.actualizar_reloj)

    # ========================================================================
    # MÉTODOS DE LA CALCULADORA
    # ========================================================================

    def calcular_riesgo_click(self):
        """Calcula el riesgo cardiovascular al hacer clic"""
        try:
            # Validar y calcular edad desde fecha de nacimiento
            mes = self.var_mes.get()
            anio = self.var_anio.get()

            if not mes or not anio:
                messagebox.showerror("Error", "Por favor ingrese la fecha de nacimiento (mes/año)")
                return

            # Calcular edad actual
            from datetime import date
            hoy = date.today()
            anio_nac = int(anio)
            mes_nac = int(mes)

            edad = hoy.year - anio_nac
            if hoy.month < mes_nac:
                edad -= 1

            # Validar otros campos requeridos
            if not self.var_pas.get():
                messagebox.showerror("Error", "Por favor ingrese la presión arterial sistólica")
                return

            if not self.var_col_total.get():
                messagebox.showerror("Error", "Por favor ingrese el colesterol total")
                return

            if not self.var_hdl.get():
                messagebox.showerror("Error", "Por favor ingrese el HDL-Cholesterol")
                return

            # Obtener valores EN MG/DL
            pas = int(self.var_pas.get())
            col_total_mgdl = float(self.var_col_total.get())
            hdl_mgdl = float(self.var_hdl.get())
            sexo = self.var_sexo.get()
            fumador = self.var_fumador.get()
            region = self.var_region.get()

            # CONVERTIR mg/dl a mmol/L para los cálculos internos
            col_total_mmol = col_total_mgdl / 38.67
            hdl_mmol = hdl_mgdl / 38.67

            # Calcular colesterol no-HDL en mmol/L (para las tablas)
            col_no_hdl_mmol = col_total_mmol - hdl_mmol

            # Calcular también en mg/dl (para mostrar)
            col_no_hdl_mgdl = col_total_mgdl - hdl_mgdl

            # # Validar rangos en mmol/L
            # if col_no_hdl_mmol < 3.0 or col_no_hdl_mmol > 7.0:
            #     messagebox.showwarning(
            #         "Advertencia",
            #         f"El colesterol no-HDL calculado ({col_no_hdl_mgdl:.1f} mg/dl) está fuera del rango válido.\n\n"
            #         f"Colesterol Total: {col_total_mgdl:.1f} mg/dl\n"
            #         f"HDL: {hdl_mgdl:.1f} mg/dl\n"
            #         f"No-HDL = Total - HDL = {col_no_hdl_mgdl:.1f} mg/dl\n\n"
            #         f"Rango válido: 116-271 mg/dl (3.0-7.0 mmol/L)"
            #     )

            # Validar rangos en mmol/L (solo advertencia, no bloquea)
            if col_no_hdl_mmol < 3.0 or col_no_hdl_mmol > 7.0:
                # Solo mostrar advertencia pero permitir continuar
                print(f"⚠️ ADVERTENCIA: Colesterol no-HDL ({col_no_hdl_mgdl:.1f} mg/dl) fuera del rango estándar.")
                print(f"   Se usará extrapolación como en HeartScore.")

            # Debug: Mostrar valores en consola
            print(f"\n{'='*60}")
            print(f"CÁLCULO DE RIESGO - DEBUG")
            print(f"{'='*60}")
            print(f"Fecha nacimiento: {mes}/{anio}")
            print(f"Edad calculada: {edad} años")
            print(f"Sexo: {sexo}")
            print(f"Fumador: {'Sí' if fumador else 'No'}")
            print(f"PAS: {pas} mmHg")
            print(f"Colesterol Total: {col_total_mgdl:.1f} mg/dl ({col_total_mmol:.2f} mmol/L)")
            print(f"HDL-Cholesterol: {hdl_mgdl:.1f} mg/dl ({hdl_mmol:.2f} mmol/L)")
            print(f"Colesterol no-HDL: {col_no_hdl_mgdl:.1f} mg/dl ({col_no_hdl_mmol:.2f} mmol/L)")
            print(f"Región seleccionada: {region}")
            print(f"{'='*60}")

            # Calcular riesgo usando valores en mmol/L
            resultado = calcular_riesgo(edad, sexo, fumador, pas, col_no_hdl_mmol, region)

            # ✅ IMPORTANTE: Agregar información adicional al resultado
            resultado['edad'] = edad
            resultado['col_total_mgdl'] = col_total_mgdl
            resultado['hdl_mgdl'] = hdl_mgdl
            resultado['col_no_hdl_mgdl'] = col_no_hdl_mgdl
            resultado['col_no_hdl_mmol'] = col_no_hdl_mmol

            print(f"RESULTADO completo: {resultado}")
            print(f"{'='*60}\n")

            if 'error' in resultado:
                messagebox.showerror("Error", resultado['error'])
                return

            # Mostrar resultados
            self.mostrar_resultado(resultado)
            self.resultado_actual = resultado

        except ValueError as e:
            messagebox.showerror("Error", f"Por favor ingrese valores numéricos válidos.\n\nDetalle: {str(e)}")
            print(f"Error de validación: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular: {str(e)}")
            print(f"Error completo: {e}")
            import traceback
            traceback.print_exc()

    def mostrar_resultado(self, resultado):
        """Muestra el resultado del cálculo"""
        # Limpiar frame
        for widget in self.resultado_frame.winfo_children():
            widget.destroy()

        # Color según categoría
        if resultado['categoria'] == 'Bajo':
            color = self.color_exito
        elif resultado['categoria'] == 'Moderado':
            color = self.color_advertencia
        else:
            color = self.color_peligro

        # Título
        ttk.Label(self.resultado_frame,
                 text=f"Riesgo Cardiovascular a 10 años",
                 font=('Segoe UI', 14, 'bold')).pack(pady=(20, 10))

        # Riesgo principal
        riesgo_label = tk.Label(self.resultado_frame,
                               text=f"{resultado['riesgo']}%",
                               font=('Segoe UI', 48, 'bold'),
                               foreground=color)
        riesgo_label.pack()

        # Categoría
        cat_frame = tk.Frame(self.resultado_frame, bg=color)
        cat_frame.pack(pady=20)

        tk.Label(cat_frame, text=f"Riesgo {resultado['categoria']}",
                font=('Segoe UI', 16, 'bold'),
                bg=color, fg='white', padx=20, pady=10).pack()

        # Detalles
        detalles_frame = ttk.LabelFrame(self.resultado_frame, text="Detalles", padding=20)
        detalles_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(detalles_frame, text=f"Edad: {resultado.get('edad', 'N/A')} años",
                 font=('Segoe UI', 10)).pack(anchor='w')
        ttk.Label(detalles_frame, text=f"Método: {resultado['score_type']}",
                 font=('Segoe UI', 10)).pack(anchor='w')
        ttk.Label(detalles_frame, text=f"Región: {resultado['region']}",
                 font=('Segoe UI', 10)).pack(anchor='w')

        # Mostrar valores de colesterol EN MG/DL
        if 'col_total_mgdl' in resultado:
            ttk.Separator(detalles_frame, orient='horizontal').pack(fill='x', pady=10)
            ttk.Label(detalles_frame, text="Valores de Colesterol:",
                     font=('Segoe UI', 10, 'bold')).pack(anchor='w')
            ttk.Label(detalles_frame,
                     text=f"• Total: {resultado['col_total_mgdl']:.1f} mg/dl",
                     font=('Segoe UI', 9)).pack(anchor='w', padx=(10, 0))
            ttk.Label(detalles_frame,
                     text=f"• HDL: {resultado['hdl_mgdl']:.1f} mg/dl",
                     font=('Segoe UI', 9)).pack(anchor='w', padx=(10, 0))
            ttk.Label(detalles_frame,
                     text=f"• no-HDL: {resultado['col_no_hdl_mgdl']:.1f} mg/dl",
                     font=('Segoe UI', 9), foreground='blue').pack(anchor='w', padx=(10, 0))

        # Interpretación
        interp_frame = ttk.LabelFrame(self.resultado_frame, text="Interpretación", padding=15)
        interp_frame.pack(fill='both', expand=True, padx=20, pady=10)

        interpretacion = self.obtener_interpretacion(resultado)
        tk.Label(interp_frame, text=interpretacion, wraplength=400,
                justify='left', font=('Segoe UI', 10)).pack()

    def obtener_interpretacion(self, resultado):
        """Retorna la interpretación del resultado"""
        riesgo = resultado['riesgo']
        categoria = resultado['categoria']

        if categoria == 'Bajo':
            return f"El paciente presenta un riesgo BAJO ({riesgo}%) de sufrir un evento cardiovascular mortal o no mortal en los próximos 10 años. Se recomienda mantener hábitos de vida saludables y controles periódicos."
        elif categoria == 'Moderado':
            return f"El paciente presenta un riesgo MODERADO ({riesgo}%) de sufrir un evento cardiovascular en los próximos 10 años. Se recomienda modificación de factores de riesgo y considerar tratamiento farmacológico según evaluación clínica."
        else:
            return f"El paciente presenta un riesgo ALTO ({riesgo}%) de sufrir un evento cardiovascular en los próximos 10 años. Se recomienda intervención intensiva con modificación de estilo de vida y tratamiento farmacológico."

    def guardar_calculo(self):
        """Guarda el cálculo actual en la base de datos"""
        if not hasattr(self, 'resultado_actual'):
            messagebox.showwarning("Advertencia", "Primero debe calcular el riesgo")
            return

        if not self.paciente_actual:
            messagebox.showwarning("Advertencia", "Debe seleccionar un paciente")
            return

        try:
            datos_calculo = {
                'paciente_id': self.paciente_actual,
                'edad': self.resultado_actual.get('edad'),
                'fumador': self.var_fumador.get(),
                'pas': int(self.var_pas.get()),
                'colesterol_no_hdl': self.resultado_actual.get('col_no_hdl_mmol'),  # Guardar en mmol/L
                'region': self.var_region.get(),
                'riesgo_porcentaje': self.resultado_actual['riesgo'],
                'categoria': self.resultado_actual['categoria'],
                'score_type': self.resultado_actual['score_type'],
                'peso': float(self.var_peso.get()) if self.var_peso.get() else None,
                'altura': float(self.var_altura.get()) if self.var_altura.get() else None,
                'colesterol_total': self.resultado_actual.get('col_total_mgdl'),  # Guardar en mg/dl
                'hdl': self.resultado_actual.get('hdl_mgdl'),  # Guardar en mg/dl
                'ldl': float(self.var_ldl.get()) if self.var_ldl.get() else None
            }

            # Calcular IMC si hay datos
            if datos_calculo['peso'] and datos_calculo['altura']:
                datos_calculo['imc'] = datos_calculo['peso'] / (datos_calculo['altura'] ** 2)

            calculo_id = self.db.agregar_calculo(datos_calculo)

            if calculo_id:
                messagebox.showinfo("Éxito", "Cálculo guardado correctamente")
                self.actualizar_lista_pacientes()
                self.cargar_historial()
            else:
                messagebox.showerror("Error", "No se pudo guardar el cálculo")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
            import traceback
            traceback.print_exc()

    # ========================================================================
    # MÉTODOS DE GESTIÓN DE PACIENTES
    # ========================================================================

    def actualizar_lista_pacientes(self):
        """Actualiza la lista de pacientes en el combo y tabla"""
        buscar = self.var_buscar.get() if hasattr(self, 'var_buscar') else ''
        pacientes = self.db.buscar_pacientes('nombre', buscar)

        # Actualizar combo
        if hasattr(self, 'combo_paciente'):
            valores = [f"{p[2]} {p[1]} (DNI: {p[3]})" for p in pacientes if p[3]]
            self.combo_paciente['values'] = valores

        # Actualizar tabla
        if hasattr(self, 'tree_pacientes'):
            self.tree_pacientes.delete(*self.tree_pacientes.get_children())
            for p in pacientes:
                edad = self.calcular_edad(p[4]) if p[4] else '-'
                self.tree_pacientes.insert('', 'end', values=(
                    p[0], p[2], p[1], p[3], edad, p[5], p[6]
                ))

    def calcular_edad(self, fecha_nac):
        """Calcula la edad a partir de la fecha de nacimiento"""
        if isinstance(fecha_nac, str):
            try:
                fecha_nac = datetime.strptime(fecha_nac, '%Y-%m-%d').date()
            except:
                return 0

        hoy = date.today()
        return hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))

    def on_paciente_seleccionado(self, event):
        """Maneja la selección de un paciente"""
        seleccion = self.combo_paciente.get()
        if seleccion:
            # Extraer DNI
            dni = seleccion.split('DNI: ')[1].rstrip(')')
            pacientes = self.db.buscar_pacientes('dni', dni)

            if pacientes:
                paciente = pacientes[0]
                self.paciente_actual = paciente[0]

                # Cargar fecha de nacimiento en formato mes/año
                if paciente[4]:  # fecha_nacimiento
                    from datetime import datetime
                    try:
                        fecha_nac = datetime.strptime(paciente[4], '%Y-%m-%d')
                        self.var_mes.set(str(fecha_nac.month))
                        self.var_anio.set(str(fecha_nac.year))
                    except:
                        pass

                self.var_sexo.set(paciente[5])

    def mostrar_nuevo_paciente(self):
        """Muestra el diálogo para crear un nuevo paciente"""
        NuevoPacienteDialog(self.root, self.db, self.actualizar_lista_pacientes)

    def exportar_paciente_pdf(self):
        """Exporta los datos completos de un paciente a PDF"""
        seleccion = self.tree_pacientes.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un paciente de la lista")
            return

        item = self.tree_pacientes.item(seleccion[0])
        paciente_id = item['values'][0]

        # Obtener datos del paciente
        paciente = self.db.obtener_paciente(paciente_id)
        if not paciente:
            messagebox.showerror("Error", "No se pudieron obtener los datos del paciente")
            return

        # Obtener cálculos del paciente
        calculos = self.db.obtener_calculos_paciente(paciente_id)

        # Seleccionar ubicación del archivo
        from datetime import datetime
        nombre_default = f"Reporte_{paciente[2]}_{paciente[1]}_{datetime.now().strftime('%Y%m%d')}.pdf"

        filename = filedialog.asksaveasfilename(
            defaultextension='.pdf',
            initialfile=nombre_default,
            filetypes=[('PDF', '*.pdf'), ('Todos', '*.*')]
        )

        if not filename:
            return

        try:
            # Intentar importar reportlab
            try:
                from reportlab.lib.pagesizes import letter, A4
                from reportlab.lib import colors
                from reportlab.lib.units import inch
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
            except ImportError:
                messagebox.showerror(
                    "Error",
                    "La librería 'reportlab' no está instalada.\n\n"
                    "Para instalarla, ejecuta:\n"
                    "pip install reportlab"
                )
                return

            # Crear el PDF
            doc = SimpleDocTemplate(filename, pagesize=A4)
            story = []
            styles = getSampleStyleSheet()

            # Estilos personalizados
            titulo_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#2563eb'),
                spaceAfter=30,
                alignment=TA_CENTER
            )

            subtitulo_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#1e40af'),
                spaceAfter=12,
                spaceBefore=12
            )

            # Encabezado
            story.append(Paragraph("REPORTE DE RIESGO CARDIOVASCULAR", titulo_style))
            story.append(Paragraph("Unidad de Prevención Cardiometabólica - ISSUNNE Corrientes", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))

            # Fecha del reporte
            fecha_reporte = datetime.now().strftime('%d/%m/%Y %H:%M')
            story.append(Paragraph(f"<b>Fecha del reporte:</b> {fecha_reporte}", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))

            # Datos del paciente
            story.append(Paragraph("DATOS DEL PACIENTE", subtitulo_style))

            datos_paciente = [
                ['Nombre completo:', f"{paciente[1]} {paciente[2]}"],
                ['DNI:', paciente[3] or 'No especificado'],
                ['Fecha de nacimiento:', paciente[4] or 'No especificada'],
                ['Sexo:', 'Masculino' if paciente[5] == 'varon' else 'Femenino'],
                ['Teléfono:', paciente[6] or 'No especificado'],
                ['Email:', paciente[7] or 'No especificado'],
                ['Obra Social:', paciente[9] or 'No especificada'],
                ['N° Afiliado:', paciente[10] or 'No especificado']
            ]

            tabla_paciente = Table(datos_paciente, colWidths=[2*inch, 4*inch])
            tabla_paciente.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))

            story.append(tabla_paciente)
            story.append(Spacer(1, 0.4*inch))

            # Historial de cálculos
            story.append(Paragraph("HISTORIAL DE EVALUACIONES DE RIESGO", subtitulo_style))

            if calculos:
                # Encabezados de la tabla
                datos_calculos = [['Fecha', 'Edad', 'Fumador', 'PAS\n(mmHg)', 'Col no-HDL\n(mg/dl)',
                                  'Riesgo\n(%)', 'Categoría', 'Método', 'Región']]

                for calc in calculos:
                    fecha = calc[2][:16] if calc[2] else ''
                    fumador = 'Sí' if calc[4] else 'No'
                    # calc[6] está en mmol/L, convertir a mg/dl para el reporte
                    col_no_hdl_mgdl = calc[6] * 38.67 if calc[6] else 0
                    col_no_hdl_texto = f"{col_no_hdl_mgdl:.1f}" if calc[6] else ''

                    datos_calculos.append([
                        fecha,
                        str(calc[3]),
                        fumador,
                        str(calc[5]),
                        col_no_hdl_texto,
                        f"{calc[8]}%",
                        calc[9],
                        calc[10],
                        calc[7].upper()
                    ])

                tabla_calculos = Table(datos_calculos, colWidths=[
                    1.1*inch, 0.5*inch, 0.6*inch, 0.6*inch, 0.7*inch, 0.6*inch, 0.8*inch, 0.7*inch, 0.7*inch
                ])

                # Estilo de la tabla
                tabla_style = [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]

                # Colores alternados en filas
                for i in range(1, len(datos_calculos)):
                    if i % 2 == 0:
                        tabla_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f8fafc')))

                    # Color según categoría de riesgo
                    categoria = datos_calculos[i][6]
                    if categoria == 'Bajo':
                        tabla_style.append(('TEXTCOLOR', (6, i), (6, i), colors.HexColor('#10b981')))
                    elif categoria == 'Moderado':
                        tabla_style.append(('TEXTCOLOR', (6, i), (6, i), colors.HexColor('#f59e0b')))
                    else:  # Alto
                        tabla_style.append(('TEXTCOLOR', (6, i), (6, i), colors.HexColor('#ef4444')))

                    tabla_style.append(('FONTNAME', (6, i), (6, i), 'Helvetica-Bold'))

                tabla_calculos.setStyle(TableStyle(tabla_style))
                story.append(tabla_calculos)

                # Último cálculo - Interpretación
                if calculos:
                    ultimo_calc = calculos[0]
                    story.append(Spacer(1, 0.3*inch))
                    story.append(Paragraph("ÚLTIMA EVALUACIÓN - INTERPRETACIÓN", subtitulo_style))

                    riesgo = ultimo_calc[8]
                    categoria = ultimo_calc[9]

                    interpretacion = self.obtener_interpretacion_detallada(riesgo, categoria)
                    story.append(Paragraph(interpretacion, styles['Normal']))

                    # Recomendaciones
                    story.append(Spacer(1, 0.2*inch))
                    story.append(Paragraph("RECOMENDACIONES", subtitulo_style))
                    recomendaciones = self.obtener_recomendaciones(categoria, ultimo_calc[4])
                    story.append(Paragraph(recomendaciones, styles['Normal']))

            else:
                story.append(Paragraph("No se han registrado evaluaciones de riesgo para este paciente.",
                                     styles['Normal']))

            # Pie de página
            story.append(Spacer(1, 0.5*inch))
            story.append(Paragraph("_" * 80, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))

            pie_texto = """
            <para align=center>
            <font size=8>
            Este reporte fue generado automáticamente por el Sistema SCORE2 de Evaluación de Riesgo Cardiovascular.<br/>
            Basado en las Guías ESC 2021 para la prevención de enfermedades cardiovasculares.<br/>
            Unidad de Prevención Cardiometabólica - ISSUNNE Corrientes Capital<br/>
            </font>
            </para>
            """
            story.append(Paragraph(pie_texto, styles['Normal']))

            # Generar PDF
            doc.build(story)

            messagebox.showinfo(
                "Éxito",
                f"Reporte PDF generado correctamente:\n\n{filename}\n\n"
                f"Paciente: {paciente[1]} {paciente[2]}\n"
                f"Cálculos incluidos: {len(calculos) if calculos else 0}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el PDF:\n\n{str(e)}")
            import traceback
            traceback.print_exc()

    def obtener_interpretacion_detallada(self, riesgo, categoria):
        """Genera interpretación detallada para el PDF"""
        if categoria == 'Bajo':
            return f"""
            El paciente presenta un riesgo BAJO ({riesgo}%) de sufrir un evento cardiovascular 
            mortal o no mortal en los próximos 10 años. Este nivel de riesgo es favorable y sugiere 
            que el paciente mantiene buenos hábitos de vida y control de factores de riesgo. Se 
            recomienda mantener el estilo de vida saludable actual y realizar controles periódicos.
            """
        elif categoria == 'Moderado':
            return f"""
            El paciente presenta un riesgo MODERADO ({riesgo}%) de sufrir un evento cardiovascular 
            en los próximos 10 años. Este nivel de riesgo indica la necesidad de intervención 
            preventiva. Se recomienda modificación intensiva del estilo de vida, control regular de 
            factores de riesgo y evaluación para tratamiento farmacológico según criterio médico.
            """
        else:  # Alto
            return f"""
            El paciente presenta un riesgo ALTO ({riesgo}%) de sufrir un evento cardiovascular en 
            los próximos 10 años. Este nivel de riesgo requiere intervención inmediata y agresiva. 
            Se recomienda tratamiento farmacológico intensivo, modificación urgente del estilo de 
            vida, y seguimiento médico estrecho. El objetivo es reducir el riesgo mediante control 
            óptimo de todos los factores modificables.
            """

    def obtener_recomendaciones(self, categoria, es_fumador):
        """Genera recomendaciones específicas para el PDF"""
        recomendaciones = []

        if es_fumador:
            recomendaciones.append("• <b>CESACIÓN TABÁQUICA URGENTE:</b> El tabaquismo es uno de los factores de riesgo más importantes y modificables. Se recomienda derivación a programa de cesación tabáquica.")

        if categoria == 'Bajo':
            recomendaciones.extend([
                "• Mantener dieta saludable tipo mediterránea",
                "• Actividad física regular (150 min/semana de intensidad moderada)",
                "• Control anual de presión arterial y perfil lipídico",
                "• Mantener peso saludable (IMC 20-25)"
            ])
        elif categoria == 'Moderado':
            recomendaciones.extend([
                "• Control de presión arterial objetivo <130/80 mmHg",
                "• Objetivo LDL-C <100 mg/dL (considerar estatinas)",
                "• Dieta estricta tipo mediterránea",
                "• Actividad física supervisada 5 días/semana",
                "• Reducción de peso si IMC >25",
                "• Seguimiento trimestral"
            ])
        else:  # Alto
            recomendaciones.extend([
                "• <b>Control estricto de PA:</b> Objetivo <130/80 mmHg con tratamiento farmacológico",
                "• <b>Terapia hipolipemiante intensiva:</b> Objetivo LDL-C <70 mg/dL",
                "• Considerar terapia antiplaquetaria (según criterio médico)",
                "• Dieta terapéutica supervisada por nutricionista",
                "• Programa estructurado de ejercicio cardiovascular",
                "• Control mensual hasta estabilización",
                "• Derivación a cardiología para evaluación complementaria"
            ])

        return "<br/>".join(recomendaciones)

    def ver_paciente(self):
        """Muestra los detalles de un paciente"""
        seleccion = self.tree_pacientes.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un paciente")
            return

        item = self.tree_pacientes.item(seleccion[0])
        paciente_id = item['values'][0]

        # Obtener datos completos
        paciente = self.db.obtener_paciente(paciente_id)
        calculos = self.db.obtener_calculos_paciente(paciente_id)

        # Crear ventana de detalles
        detalle_window = tk.Toplevel(self.root)
        detalle_window.title(f"Detalles del Paciente")
        detalle_window.geometry("600x500")

        # Frame con scroll
        canvas = tk.Canvas(detalle_window)
        scrollbar = ttk.Scrollbar(detalle_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Datos del paciente
        ttk.Label(scrollable_frame, text=f"{paciente[1]} {paciente[2]}",
                 font=('Segoe UI', 16, 'bold')).pack(pady=10)

        info_frame = ttk.LabelFrame(scrollable_frame, text="Información Personal", padding=10)
        info_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(info_frame, text=f"DNI: {paciente[3] or 'No especificado'}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Fecha de nacimiento: {paciente[4] or 'No especificada'}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Sexo: {'Masculino' if paciente[5] == 'varon' else 'Femenino'}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Teléfono: {paciente[6] or 'No especificado'}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Email: {paciente[7] or 'No especificado'}").pack(anchor='w')

        # Resumen de riesgo
        if calculos:
            resumen_frame = ttk.LabelFrame(scrollable_frame, text="Última Evaluación", padding=10)
            resumen_frame.pack(fill='x', padx=20, pady=10)

            ultimo = calculos[0]
            ttk.Label(resumen_frame, text=f"Fecha: {ultimo[2]}").pack(anchor='w')
            ttk.Label(resumen_frame, text=f"Riesgo: {ultimo[8]}%",
                     font=('Segoe UI', 14, 'bold')).pack(anchor='w')
            ttk.Label(resumen_frame, text=f"Categoría: {ultimo[9]}").pack(anchor='w')
            ttk.Label(resumen_frame, text=f"Total de evaluaciones: {len(calculos)}").pack(anchor='w')

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def editar_paciente(self):
        """Permite editar un paciente"""
        seleccion = self.tree_pacientes.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un paciente")
            return

        item = self.tree_pacientes.item(seleccion[0])
        paciente_id = item['values'][0]

        # Por ahora solo mostramos mensaje
        messagebox.showinfo("Editar Paciente",
                           "Función de edición en desarrollo.\n"
                           "Por ahora puede crear un nuevo paciente con los datos actualizados.")

    def eliminar_paciente(self):
        """Elimina un paciente y actualiza la vista"""
        seleccion = self.tree_pacientes.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un paciente de la lista")
            return

        item = self.tree_pacientes.item(seleccion[0])
        paciente_id = item['values'][0]
        nombre_paciente = f"{item['values'][1]}, {item['values'][2]}"

        respuesta = messagebox.askyesnocancel(
            "Eliminar Paciente",
            f"¿Cómo desea eliminar al paciente '{nombre_paciente}'?\n\n"
            f"• SÍ: Eliminación lógica (ocultar de la lista)\n"
            f"• NO: Eliminación física (borrar completamente)\n"
            f"• CANCELAR: No eliminar",
            icon='question'
        )

        if respuesta is None:  # Cancel
            return
        elif respuesta:  # Yes - Eliminación lógica
            if self.db.eliminar_paciente(paciente_id, soft_delete=True):
                messagebox.showinfo("Éxito",
                    "Paciente ocultado correctamente.\n"
                    "El paciente ya no aparecerá en la lista pero sus datos se conservan en la base de datos.")
                self.actualizar_lista_pacientes()
                self.cargar_historial()
        else:  # No - Eliminación física
            confirmacion = messagebox.askyesno(
                "⚠️ Confirmación Final",
                "¿Está COMPLETAMENTE SEGURO?\n\n"
                "Esta acción eliminará PERMANENTEMENTE:\n"
                "• Datos del paciente\n"
                "• Todos sus cálculos de riesgo\n"
                "• Todo su historial\n\n"
                "Esta operación NO SE PUEDE DESHACER.",
                icon='warning'
            )

            if confirmacion:
                if self.db.eliminar_paciente(paciente_id, soft_delete=False):
                    messagebox.showinfo("Eliminado", "Paciente eliminado permanentemente de la base de datos.")
                    self.actualizar_lista_pacientes()
                    self.cargar_historial()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el paciente")

    # ========================================================================
    # MÉTODOS DE ESTADÍSTICAS
    # ========================================================================

    def actualizar_estadisticas(self):
        """Actualiza las estadísticas generales"""
        stats = self.db.obtener_estadisticas()

        if not stats:
            return

        # Limpiar frame
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        # Crear cards
        metricas = [
            ("Total Pacientes", stats[0], self.color_primario),
            ("Total Cálculos", stats[1], self.color_secundario),
            ("Riesgo Promedio", f"{stats[2]:.1f}%", self.color_advertencia),
            ("Riesgo Bajo", stats[3], self.color_exito),
            ("Riesgo Moderado", stats[4], self.color_advertencia),
            ("Riesgo Alto", stats[5], self.color_peligro)
        ]

        for i, (titulo, valor, color) in enumerate(metricas):
            self.crear_card_metrica(self.cards_frame, titulo, valor, color, i)

    def crear_card_metrica(self, parent, titulo, valor, color, posicion):
        """Crea una tarjeta de métrica"""
        card = tk.Frame(parent, bg=color)
        card.grid(row=posicion//3, column=posicion%3, padx=10, pady=10, sticky='ew')

        tk.Label(card, text=str(valor), font=('Segoe UI', 24, 'bold'),
                bg=color, fg='white').pack(pady=(15, 5), padx=20)
        tk.Label(card, text=titulo, font=('Segoe UI', 10),
                bg=color, fg='white').pack(pady=(0, 15), padx=20)

        parent.columnconfigure(posicion%3, weight=1)

    def mostrar_estadisticas(self):
        """Muestra el dashboard de estadísticas"""
        self.notebook.select(self.tab_estadisticas)
        self.actualizar_estadisticas()

    def mostrar_graficos(self):
        """Muestra gráficos estadísticos"""
        messagebox.showinfo("Info", "Función de gráficos en desarrollo")

    # ========================================================================
    # OTRAS FUNCIONES
    # ========================================================================

    def exportar_csv(self):
        """Exporta los datos a CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV', '*.csv'), ('Todos', '*.*')]
        )

        if filename:
            if self.db.exportar_a_csv(filename):
                messagebox.showinfo("Éxito", f"Datos exportados a {filename}")
            else:
                messagebox.showerror("Error", "No se pudo exportar")

    def crear_backup(self):
        """Crea un backup de la base de datos"""
        backup_file = self.db.backup_database()
        if backup_file:
            messagebox.showinfo("Éxito", f"Backup creado: {backup_file}")
        else:
            messagebox.showerror("Error", "No se pudo crear el backup")

    def buscar_paciente(self):
        """Activa la búsqueda de pacientes"""
        self.notebook.select(self.tab_pacientes)

    def mostrar_lista_pacientes(self):
        """Muestra la lista de pacientes"""
        self.notebook.select(self.tab_pacientes)

    def mostrar_acerca_de(self):
        """Muestra información sobre la aplicación"""
        messagebox.showinfo(
            "Acerca de",
            "SCORE2 - Calculadora de Riesgo Cardiovascular\n\n"
            "Versión 1.0\n\n"
            "Unidad de Prevención Cardiometabólica\n"
            "ISSUNNE - Corrientes Capital\n\n"
            "Basado en Guías ESC 2021"
        )

    def mostrar_guia(self):
        """Muestra la guía de uso"""
        messagebox.showinfo(
            "Guía de Uso",
            "1. Cree o seleccione un paciente\n"
            "2. Complete los datos clínicos\n"
            "3. Presione 'Calcular Riesgo'\n"
            "4. Revise los resultados\n"
            "5. Guarde el cálculo en la base de datos"
        )


# ============================================================================
# DIÁLOGOS AUXILIARES
# ============================================================================

class NuevoPacienteDialog:
    """Diálogo para crear un nuevo paciente"""

    def __init__(self, parent, db, callback):
        self.db = db
        self.callback = callback

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nuevo Paciente")
        self.dialog.geometry("600x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.crear_formulario()

    def crear_formulario(self):
        """Crea el formulario de nuevo paciente"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)

        # Título
        ttk.Label(main_frame, text="Datos del Paciente",
                 font=('Segoe UI', 14, 'bold')).grid(
            row=0, column=0, columnspan=2, pady=10)

        row = 1

        # Campos del formulario
        campos = [
            ('Nombre*:', 'nombre'),
            ('Apellido*:', 'apellido'),
            ('DNI:', 'dni'),
            ('Fecha Nacimiento:', 'fecha_nac'),
            ('Teléfono:', 'telefono'),
            ('Email:', 'email'),
            ('Dirección:', 'direccion'),
            ('Obra Social:', 'obra_social'),
            ('N° Afiliado:', 'numero_afiliado')
        ]

        self.vars = {}

        for label, key in campos:
            ttk.Label(main_frame, text=label).grid(row=row, column=0, sticky='w', pady=5)

            self.vars[key] = tk.StringVar()
            entry = ttk.Entry(main_frame, textvariable=self.vars[key])
            entry.grid(row=row, column=1, sticky='ew', pady=5)

            # Placeholder para fecha de nacimiento
            if key == 'fecha_nac':
                entry.insert(0, 'DD/MM/AAAA')
                entry.config(foreground='gray')

                def on_focus_in(e):
                    if entry.get() == 'DD/MM/AAAA':
                        entry.delete(0, tk.END)
                        entry.config(foreground='black')

                def on_focus_out(e):
                    if not entry.get():
                        entry.insert(0, 'DD/MM/AAAA')
                        entry.config(foreground='gray')

                entry.bind('<FocusIn>', on_focus_in)
                entry.bind('<FocusOut>', on_focus_out)

            row += 1

        # Sexo
        ttk.Label(main_frame, text="Sexo*:").grid(row=row, column=0, sticky='w', pady=5)
        self.vars['sexo'] = tk.StringVar(value='varon')
        sexo_frame = ttk.Frame(main_frame)
        sexo_frame.grid(row=row, column=1, sticky='w', pady=5)
        ttk.Radiobutton(sexo_frame, text="Varón", variable=self.vars['sexo'],
                       value='varon').pack(side='left')
        ttk.Radiobutton(sexo_frame, text="Mujer", variable=self.vars['sexo'],
                       value='mujer').pack(side='left', padx=10)
        row += 1

        # Observaciones
        ttk.Label(main_frame, text="Observaciones:").grid(
            row=row, column=0, sticky='nw', pady=5)
        self.vars['observaciones'] = tk.Text(main_frame, height=4, width=40)
        self.vars['observaciones'].grid(row=row, column=1, sticky='ew', pady=5)
        row += 1

        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.dialog.destroy).pack(side='left', padx=5)

        main_frame.columnconfigure(1, weight=1)

    def guardar(self):
        """Guarda el nuevo paciente"""
        # Validar campos obligatorios
        if not self.vars['nombre'].get() or not self.vars['apellido'].get():
            messagebox.showwarning("Advertencia", "Complete los campos obligatorios")
            return

        # Preparar datos
        datos = {
            'nombre': self.vars['nombre'].get(),
            'apellido': self.vars['apellido'].get(),
            'dni': self.vars['dni'].get(),
            'fecha_nacimiento': self.vars['fecha_nac'].get(),
            'sexo': self.vars['sexo'].get(),
            'telefono': self.vars['telefono'].get(),
            'email': self.vars['email'].get(),
            'direccion': self.vars['direccion'].get(),
            'obra_social': self.vars['obra_social'].get(),
            'numero_afiliado': self.vars['numero_afiliado'].get(),
            'observaciones': self.vars['observaciones'].get('1.0', 'end-1c')
        }

        # Guardar
        paciente_id = self.db.agregar_paciente(datos)

        if paciente_id:
            messagebox.showinfo("Éxito", "Paciente registrado correctamente")
            self.callback()
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar el paciente")


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

def main():
    root = tk.Tk()
    app = SCORE2App(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n✓ Aplicación cerrada por el usuario")

if __name__ == "__main__":
    main()