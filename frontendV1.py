import customtkinter as ctk
from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from chatSinox import AplicacionChatbot

SUPABASE_URL = "https://jvrarglskymgrjfvgyuy.supabase.co"
SUPABASE_KEY = "TU_CLAVE_SUPABASE" 

COLOR_FONDO_PRINCIPAL = "#030a21"
COLOR_FONDO_TARJETA   = "#042b62"
COLOR_BOTON_NORMAL    = "#5884b0"
COLOR_BOTON_HOVER     = "#5f8ebd"
COLOR_CUADRO_IMAGEN   = "#7da1c3"
COLOR_TEXTO           = "#c8eaff"
COLOR_TEXTO_OSCURO    = "#030a21"
COLOR_ERROR           = "#ef4444"
COLOR_EXITO           = "#10b981"

ctk.set_appearance_mode("dark")

def limpiar_pantalla(contenedor):
    for widget in contenedor.winfo_children():
        widget.destroy()

def vista_registro_clientes(contenedor):
    titulo = ctk.CTkLabel(contenedor, text="Registro de Clientes", font=("Roboto", 24, "bold"), text_color=COLOR_TEXTO)
    titulo.pack(pady=(0, 20), anchor="w")

    frame_formulario = ctk.CTkFrame(contenedor, fg_color=COLOR_FONDO_TARJETA, corner_radius=15)
    frame_formulario.pack(fill="x", padx=20, pady=10)

    campos = ["Nombre Completo", "Ingresos Mensuales ($)", "Historial Crediticio (Puntaje)", "Datos de Contacto (Email/Tel)"]
    entradas = {}

    for i, campo in enumerate(campos):
        lbl = ctk.CTkLabel(frame_formulario, text=campo, text_color=COLOR_TEXTO, font=("Roboto", 14))
        lbl.grid(row=i, column=0, padx=20, pady=15, sticky="w")
        
        ent = ctk.CTkEntry(frame_formulario, width=300, fg_color=COLOR_FONDO_PRINCIPAL, border_color=COLOR_BOTON_NORMAL, text_color=COLOR_TEXTO)
        ent.grid(row=i, column=1, padx=20, pady=15, sticky="w")
        entradas[campo] = ent

    def guardar_cliente_mock():
        messagebox.showinfo("Éxito", "Cliente registrado exitosamente (Mock).")
        for ent in entradas.values():
            ent.delete(0, ctk.END)

    btn_guardar = ctk.CTkButton(frame_formulario, text="Registrar Cliente", fg_color=COLOR_BOTON_NORMAL, hover_color=COLOR_BOTON_HOVER, command=guardar_cliente_mock)
    btn_guardar.grid(row=len(campos), column=0, columnspan=2, pady=20)

def vista_gestion_creditos(contenedor):
    titulo = ctk.CTkLabel(contenedor, text="Gestión de Créditos", font=("Roboto", 24, "bold"), text_color=COLOR_TEXTO)
    titulo.pack(pady=(0, 20), anchor="w")

    frame_tabla = ctk.CTkFrame(contenedor, fg_color=COLOR_FONDO_TARJETA, corner_radius=15)
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    lbl_info = ctk.CTkLabel(frame_tabla, text="[Aquí se renderizará la tabla de créditos activos usando Treeview o CTkScrollableFrame]", text_color=COLOR_CUADRO_IMAGEN)
    lbl_info.pack(pady=50)

    frame_acciones = ctk.CTkFrame(contenedor, fg_color="transparent")
    frame_acciones.pack(fill="x", padx=20, pady=10)

    ctk.CTkButton(frame_acciones, text="Aprobar Nuevo Crédito", fg_color=COLOR_EXITO, hover_color="#059669").pack(side="left", padx=10)
    ctk.CTkButton(frame_acciones, text="Actualizar Estado", fg_color=COLOR_BOTON_NORMAL, hover_color=COLOR_BOTON_HOVER).pack(side="left", padx=10)

def vista_control_pagos(contenedor):
    titulo = ctk.CTkLabel(contenedor, text="Control de Pagos", font=("Roboto", 24, "bold"), text_color=COLOR_TEXTO)
    titulo.pack(pady=(0, 20), anchor="w")

    frame_pagos = ctk.CTkFrame(contenedor, fg_color=COLOR_FONDO_TARJETA, corner_radius=15)
    frame_pagos.pack(fill="x", padx=20, pady=10)

    ctk.CTkLabel(frame_pagos, text="ID de Crédito:", text_color=COLOR_TEXTO).grid(row=0, column=0, padx=20, pady=15)
    ctk.CTkEntry(frame_pagos, placeholder_text="Ej. CRED-001", fg_color=COLOR_FONDO_PRINCIPAL, border_color=COLOR_BOTON_NORMAL).grid(row=0, column=1, padx=20, pady=15)

    ctk.CTkLabel(frame_pagos, text="Monto a Abonar:", text_color=COLOR_TEXTO).grid(row=1, column=0, padx=20, pady=15)
    ctk.CTkEntry(frame_pagos, placeholder_text="$ 0.00", fg_color=COLOR_FONDO_PRINCIPAL, border_color=COLOR_BOTON_NORMAL).grid(row=1, column=1, padx=20, pady=15)

    ctk.CTkButton(frame_pagos, text="Registrar Pago y Calcular Interés", fg_color=COLOR_BOTON_NORMAL, hover_color=COLOR_BOTON_HOVER).grid(row=2, column=0, columnspan=2, pady=20)

def vista_busqueda_avanzada(contenedor):
    titulo = ctk.CTkLabel(contenedor, text="Búsqueda Avanzada", font=("Roboto", 24, "bold"), text_color=COLOR_TEXTO)
    titulo.pack(pady=(0, 20), anchor="w")

    frame_busqueda = ctk.CTkFrame(contenedor, fg_color="transparent")
    frame_busqueda.pack(fill="x", padx=20, pady=10)

    ctk.CTkEntry(frame_busqueda, placeholder_text="Buscar por nombre, estado, fecha...", width=400, fg_color=COLOR_FONDO_PRINCIPAL, border_color=COLOR_BOTON_NORMAL).pack(side="left", padx=(0,10))
    ctk.CTkButton(frame_busqueda, text="Buscar", fg_color=COLOR_BOTON_NORMAL, hover_color=COLOR_BOTON_HOVER).pack(side="left")

    frame_resultados = ctk.CTkFrame(contenedor, fg_color=COLOR_FONDO_TARJETA, corner_radius=15)
    frame_resultados.pack(fill="both", expand=True, padx=20, pady=10)
    ctk.CTkLabel(frame_resultados, text="[Resultados de búsqueda aparecerán aquí]", text_color=COLOR_CUADRO_IMAGEN).pack(pady=50)

def vista_reportes_analisis(contenedor):
    titulo = ctk.CTkLabel(contenedor, text="Análisis de Datos y Reportes", font=("Roboto", 24, "bold"), text_color=COLOR_TEXTO)
    titulo.pack(pady=(0, 20), anchor="w")

    frame_graficos = ctk.CTkFrame(contenedor, fg_color="transparent")
    frame_graficos.pack(fill="both", expand=True, padx=20, pady=10)

    grafico1 = ctk.CTkFrame(frame_graficos, fg_color=COLOR_FONDO_TARJETA, corner_radius=15, width=300, height=200)
    grafico1.pack(side="left", fill="both", expand=True, padx=10)
    ctk.CTkLabel(grafico1, text="Gráfico de Dispersión\n(Ingresos vs Riesgo)", text_color=COLOR_TEXTO).place(relx=0.5, rely=0.5, anchor="center")

    grafico2 = ctk.CTkFrame(frame_graficos, fg_color=COLOR_FONDO_TARJETA, corner_radius=15, width=300, height=200)
    grafico2.pack(side="right", fill="both", expand=True, padx=10)
    ctk.CTkLabel(grafico2, text="Tendencias de Ingresos\n(Cobro de Intereses)", text_color=COLOR_TEXTO).place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkButton(contenedor, text="Exportar Reporte (PDF/Excel)", fg_color=COLOR_BOTON_NORMAL, hover_color=COLOR_BOTON_HOVER).pack(pady=20)

def mostrar_menu_principal(ventana):
    limpiar_pantalla(ventana)
    ventana.geometry("1000x700")
    ventana.title("Sistema de Gestión de Créditos Bancarios")

    ventana_chatbot = ctk.CTkToplevel(ventana)
    ventana_chatbot.title("Asistente Sinox AI")
    ventana_chatbot.geometry("450x650") 
    ventana_chatbot.attributes("-topmost", True) 

    asistente_ia = AplicacionChatbot(ventana_chatbot)

    sidebar = ctk.CTkFrame(ventana, width=250, corner_radius=0, fg_color=COLOR_FONDO_TARJETA)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    ctk.CTkLabel(sidebar, text="Bank Admin", font=("Roboto", 24, "bold"), text_color=COLOR_TEXTO).pack(pady=(30, 40))

    main_content = ctk.CTkFrame(ventana, corner_radius=0, fg_color=COLOR_FONDO_PRINCIPAL)
    main_content.pack(side="right", fill="both", expand=True, padx=30, pady=30)

    def cambiar_vista(vista_func, nombre_vista="General"):
        limpiar_pantalla(main_content)
        vista_func(main_content)
        
        if hasattr(asistente_ia, 'actualizar_contexto'):
            asistente_ia.actualizar_contexto(nombre_vista)

    opciones = [
        ("Registro de Clientes", vista_registro_clientes),
        ("Gestión de Créditos", vista_gestion_creditos),
        ("Control de Pagos", vista_control_pagos),
        ("Búsqueda Avanzada", vista_busqueda_avanzada),
        ("Reportes y Análisis", vista_reportes_analisis)
    ]

    for texto, funcion in opciones:
        btn = ctk.CTkButton(
            sidebar, 
            text=texto, 
            fg_color="transparent", 
            hover_color=COLOR_BOTON_NORMAL,
            text_color=COLOR_TEXTO,
            font=("Roboto", 14),
            anchor="w",
            command=lambda f=funcion, t=texto: cambiar_vista(f, t)
        )
        btn.pack(fill="x", padx=20, pady=10)

    btn_cerrar = ctk.CTkButton(sidebar, text="Cerrar Sesión", fg_color=COLOR_ERROR, hover_color="#b91c1c", command=lambda: mostrar_pantalla_login(ventana))
    btn_cerrar.pack(side="bottom", pady=30, padx=20, fill="x")

    cambiar_vista(vista_registro_clientes, "Registro de Clientes")

def mostrar_pantalla_login(ventana):
    limpiar_pantalla(ventana)
    ventana.geometry("600x600")
    ventana.title("Inicio de Sesión - Gestión de Créditos")

    frame_login = ctk.CTkFrame(ventana, corner_radius=20, fg_color=COLOR_FONDO_TARJETA)
    frame_login.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    label_titulo = ctk.CTkLabel(frame_login, text="Acceso al Sistema", font=("Roboto", 24, "bold"), text_color=COLOR_TEXTO)
    label_titulo.pack(pady=(30, 10), padx=40)

    frame_imagen = ctk.CTkFrame(frame_login, width=150, height=150, fg_color=COLOR_CUADRO_IMAGEN, corner_radius=75)
    frame_imagen.pack(pady=10)

    entry_usuario = ctk.CTkEntry(
        frame_login, placeholder_text="Nombre de usuario", width=250, height=40, corner_radius=10,
        text_color=COLOR_TEXTO, fg_color=COLOR_FONDO_PRINCIPAL, border_color=COLOR_BOTON_NORMAL
    )
    entry_usuario.pack(pady=10)

    entry_password = ctk.CTkEntry(
        frame_login, placeholder_text="Contraseña", show="*", width=250, height=40, corner_radius=10,
        text_color=COLOR_TEXTO, fg_color=COLOR_FONDO_PRINCIPAL, border_color=COLOR_BOTON_NORMAL
    )
    entry_password.pack(pady=10)

    label_error = ctk.CTkLabel(frame_login, text="", text_color=COLOR_ERROR, font=("Roboto", 12))
    label_error.pack(pady=5)

    def validar_login():
        usr = entry_usuario.get()
        pwd = entry_password.get()
        if usr != "" and pwd != "":
            mostrar_menu_principal(ventana)
        else:
            label_error.configure(text="Por favor, ingrese sus credenciales.")

    btn_ingresar = ctk.CTkButton(
        frame_login, text="Ingresar", fg_color=COLOR_BOTON_NORMAL, hover_color=COLOR_BOTON_HOVER,
        text_color=COLOR_TEXTO, font=("Roboto", 14, "bold"), command=validar_login
    )
    btn_ingresar.pack(pady=(10, 30))

def iniciar_aplicacion():
    ventana = ctk.CTk()
    ventana.configure(fg_color=COLOR_FONDO_PRINCIPAL)
    mostrar_pantalla_login(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    iniciar_aplicacion()
