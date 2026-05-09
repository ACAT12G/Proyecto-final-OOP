import tkinter as tk
from tkinter import ttk, messagebox
from backendV1 import *

class SistemaCreditosApp(tk.Tk):
    #Ventana principal del sistema de gestión
    
    def __init__(self):

        super().__init__()
        self.title("Sistema de Gestión de Créditos Bancarios")
        self.geometry("900x600")
        self.configure(bg="#272766")
        
        # Variables de control de UI
        self.busqueda_avanzada = Busqueda_Avanzada()
        
        self._configurar_estilos()
        self._crear_widgets()

    def _configurar_estilos(self):

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook.Tab", font=("Helvetica", 11, "bold"), padding=[10, 5])
        style.configure("TLabel", font=("Helvetica", 10), background="#f4f4f9")
        style.configure("TButton", font=("Helvetica", 10, "bold"), background="#004aad", foreground="white")
        style.map("TButton", background=[("active", "#003080")])

    def _crear_widgets(self):
        #Crea el sistema de pestañas para organizar los módulos
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Creación de Frames para cada módulo
        self.frame_clientes = ttk.Frame(self.notebook, padding=15)
        self.frame_creditos = ttk.Frame(self.notebook, padding=15)
        self.frame_analisis = ttk.Frame(self.notebook, padding=15)
        self.frame_pagos = ttk.Frame(self.notebook, padding=15)

        self.notebook.add(self.frame_clientes, text="Registro de Clientes")
        self.notebook.add(self.frame_creditos, text="Gestión de Créditos")
        self.notebook.add(self.frame_pagos, text="Gestión de Pagos")
        self.notebook.add(self.frame_analisis, text="Análisis y Reportes")
        

        self._construir_modulo_clientes()
        self._construir_modulo_creditos()
        self._construir_modulo_pagos()
        self._construir_modulo_analisis()


    # MÓDULO: REGISTRO DE CLIENTES
    
    def _construir_modulo_clientes(self):
        #Construye la interfaz para registrar nuevos clientes
        ttk.Label(self.frame_clientes, text="Registrar Nuevo Cliente", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        # Campos de entrada
        ttk.Label(self.frame_clientes, text="Nombre Completo:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_nombre = ttk.Entry(self.frame_clientes, width=40)
        self.entry_nombre.grid(row=1, column=1, pady=5)

        ttk.Label(self.frame_clientes, text="Ingresos Mensuales ($):").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_ingresos = ttk.Entry(self.frame_clientes, width=40)
        self.entry_ingresos.grid(row=2, column=1, pady=5)

        ttk.Label(self.frame_clientes, text="Historial Crediticio:").grid(row=3, column=0, sticky="w", pady=5)
        self.combo_historial = ttk.Combobox(self.frame_clientes, values=["Excelente", "Bueno", "Regular", "Malo"], state="readonly", width=37)
        self.combo_historial.set("Bueno")
        self.combo_historial.grid(row=3, column=1, pady=5)

        ttk.Label(self.frame_clientes, text="Datos de Contacto (Email/Tel):").grid(row=4, column=0, sticky="w", pady=5)
        self.entry_contacto = ttk.Entry(self.frame_clientes, width=40)
        self.entry_contacto.grid(row=4, column=1, pady=5)

        # Botón de guardado
        btn_guardar = ttk.Button(self.frame_clientes, text="Guardar Cliente", command=self.guardar_cliente)
        btn_guardar.grid(row=5, column=1, sticky="e", pady=15)

    def guardar_cliente(self):
        #Instancia la clase Reg_Clientes y guarda los datos
        nombre = self.entry_nombre.get()
        try:
            ingresos = float(self.entry_ingresos.get())
        except ValueError:
            messagebox.showerror("Error", "Los ingresos deben ser un valor numérico.")
            return
            
        historial = self.combo_historial.get()
        contacto = self.entry_contacto.get()

        if not nombre or not contacto:
            messagebox.showwarning("Advertencia", "Por favor, llene todos los campos requeridos.")
            return

        # Aplicación de POO para manejar la lógica de guardado
        nuevo_cliente = Reg_Clientes(nombre, ingresos, historial, contacto)
        if nuevo_cliente.guardar():
            messagebox.showinfo("Éxito", f"Cliente {nombre} registrado correctamente.")
            self.entry_nombre.delete(0, tk.END)
            self.entry_ingresos.delete(0, tk.END)
            self.entry_contacto.delete(0, tk.END)
        else:
            messagebox.showerror("Error de Conexión", "No se pudo guardar el cliente en la base de datos. Verifica tus credenciales de Supabase.")

   
    # MÓDULO: GESTIÓN DE CRÉDITOS
    
    def _construir_modulo_creditos(self):
        #Construye la interfaz para la asignación y cálculo de créditos
        ttk.Label(self.frame_creditos, text="Otorgar Crédito", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        ttk.Label(self.frame_creditos, text="ID del Cliente:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_id_cliente = ttk.Entry(self.frame_creditos, width=30)
        self.entry_id_cliente.grid(row=1, column=1, pady=5)

        ttk.Label(self.frame_creditos, text="Monto a Otorgar ($):").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_monto = ttk.Entry(self.frame_creditos, width=30)
        self.entry_monto.grid(row=2, column=1, pady=5)

        ttk.Label(self.frame_creditos, text="Tasa de Interés Anual (%):").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_tasa = ttk.Entry(self.frame_creditos, width=30)
        self.entry_tasa.grid(row=3, column=1, pady=5)

        ttk.Label(self.frame_creditos, text="Plazo (Meses):").grid(row=4, column=0, sticky="w", pady=5)
        self.entry_plazo = ttk.Entry(self.frame_creditos, width=30)
        self.entry_plazo.grid(row=4, column=1, pady=5)

        btn_calcular = ttk.Button(self.frame_creditos, text="Calcular y Guardar Crédito", command=self.procesar_credito)
        btn_calcular.grid(row=5, column=1, sticky="e", pady=15)
        
        self.lbl_resultado_pago = ttk.Label(self.frame_creditos, text="", font=("Helvetica", 11, "bold"), foreground="green")
        self.lbl_resultado_pago.grid(row=6, column=0, columnspan=2, pady=10)

    def procesar_credito(self):
        #Calcula el pago mensual y guarda el crédito mediante la clase Gestion_Creditos
        try:
            cliente_id = int(self.entry_id_cliente.get())
            monto = float(self.entry_monto.get())
            tasa = float(self.entry_tasa.get())
            plazo = int(self.entry_plazo.get())
        except ValueError:
            messagebox.showerror("Error", "Verifique que todos los campos sean numéricos.")
            return

        # Instancia de la clase de créditos
        nuevo_credito = Gestion_Creditos(cliente_id, monto, tasa, plazo)
        
        if nuevo_credito.guardar():
            self.lbl_resultado_pago.config(text=f"Crédito Aprobado. Pago Mensual Calculado: ${nuevo_credito.pago_mensual:,.2f}")
        else:
             messagebox.showerror("Error", "Fallo al registrar el crédito en Supabase.")

    #MODULO: PAGOS

    def _construir_modulo_pagos(self):
        # Construye la interfaz para registrar abonos y morosidad
        ttk.Label(self.frame_pagos, text="Registrar Pago a Crédito", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        ttk.Label(self.frame_pagos, text="ID del Crédito:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_pago_id_credito = ttk.Entry(self.frame_pagos, width=30)
        self.entry_pago_id_credito.grid(row=1, column=1, pady=5)

        ttk.Label(self.frame_pagos, text="Monto a Abonar ($):").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_pago_monto = ttk.Entry(self.frame_pagos, width=30)
        self.entry_pago_monto.grid(row=2, column=1, pady=5)

        ttk.Label(self.frame_pagos, text="Días de Retraso (Dejar en 0 si es puntual):").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_pago_retraso = ttk.Entry(self.frame_pagos, width=30)
        self.entry_pago_retraso.insert(0, "0") # Valor por defecto
        self.entry_pago_retraso.grid(row=3, column=1, pady=5)

        btn_registrar_pago = ttk.Button(self.frame_pagos, text="Aplicar Pago", command=self.procesar_pago)
        btn_registrar_pago.grid(row=4, column=1, sticky="e", pady=15)

    def procesar_pago(self):
        try:
            id_credito = int(self.entry_pago_id_credito.get())
            monto_abonar = float(self.entry_pago_monto.get())
            dias_retraso = int(self.entry_pago_retraso.get())
        except ValueError:
            messagebox.showerror("Error", "Verifique que todos los campos sean numéricos.")
            return

        try:
            # 1. Instanciamos el controlador de pagos vinculado al crédito
            gestor_pagos = Control_Pagos(id_credito)
            
            # si hay mora, calculamos la penalización antes de registrar
            # Asumimos una penalización de ejemplo del 2% por mora
            penalizacion = 0
            if dias_retraso > 0:
                penalizacion = gestor_pagos.calcular_moratorios(dias_retraso, tasa_penalizacion=2.0)
                messagebox.showwarning("Atención", f"Se han calculado ${penalizacion:,.2f} de intereses moratorios por {dias_retraso} días de retraso.")

            # 3. Guardamos el registro en Supabase
            gestor_pagos.registrar_pago(monto_abonar)
            
            messagebox.showinfo("Éxito", "Pago registrado exitosamente en la base de datos.")
            
            # Limpiamos los campos
            self.entry_pago_id_credito.delete(0, tk.END)
            self.entry_pago_monto.delete(0, tk.END)
            self.entry_pago_retraso.delete(0, tk.END)
            self.entry_pago_retraso.insert(0, "0")

        except Exception as e:
            print(f"Error al procesar pago: {e}")
            messagebox.showerror("Error de Conexión", "No se pudo registrar el pago. Verifique el ID del crédito.")

    
    # MÓDULO: ANÁLISIS DE DATOS
   
    def _construir_modulo_analisis(self):
        #Botones interactivos para visualizar los datos de la cartera de clientes
        ttk.Label(self.frame_analisis, text="Herramientas de Análisis Data-Driven", font=("Helvetica", 14, "bold")).pack(pady=20)
        
        btn_dispersion = ttk.Button(self.frame_analisis, text="Generar Gráfico de Dispersión (Ingresos vs Impago)", 
                                    command=self.mostrar_grafico, width=50)
        btn_dispersion.pack(pady=10)
        
        ttk.Label(self.frame_analisis, text="Asegúrate de tener datos registrados en Supabase para visualizar las gráficas.", foreground="gray").pack(pady=20)

    def mostrar_grafico(self):
        #Llama al método estático de la clase Analisis_Datos
        exito = Analisis_Datos.generar_grafico_dispersion()
        if not exito:
            messagebox.showwarning("Datos Insuficientes", "No hay datos suficientes en la base de datos para graficar.")

if __name__ == "__main__":
    app = SistemaCreditosApp()
    app.mainloop()