import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from chatSinox import AplicacionChatbot
from backendV2 import *
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

COLOR_FONDO_PRINCIPAL = "#030a21"
COLOR_FONDO_TARJETA   = "#042b62"
COLOR_BOTON_NORMAL    = "#5884b0"
COLOR_BOTON_HOVER     = "#5f8ebd"
COLOR_CUADRO_IMAGEN   = "#7da1c3"
COLOR_TEXTO           = "#c8eaff"
COLOR_ERROR           = "#ef4444"
COLOR_EXITO           = "#10b981"

ctk.set_appearance_mode("dark")

def limpiar_pantalla(contenedor):
    for widget in contenedor.winfo_children(): widget.destroy()

def vista_registro_clientes(contenedor):
    limpiar_pantalla(contenedor)
    ctk.CTkLabel(contenedor, text="Registro de Clientes", font=("Roboto", 24, "bold"), text_color=COLOR_TEXTO).pack(pady=(0, 20), anchor="w")
    frame = ctk.CTkFrame(contenedor, fg_color=COLOR_FONDO_TARJETA, corner_radius=15)
    frame.pack(fill="x", padx=20, pady=10)
    
    campos = ["Nombre Completo", "Ingresos Mensuales ($)", "Historial Crediticio", "Datos de Contacto"]
    entradas = {}
    
    for i, campo in enumerate(campos):
        ctk.CTkLabel(frame, text=campo, text_color=COLOR_TEXTO, font=("Roboto", 14)).grid(row=i, column=0, padx=20, pady=15, sticky="w")
        if campo == "Historial Crediticio":
            ent = ctk.CTkComboBox(frame, values=["Excelente", "Bueno", "Regular", "Malo"], width=300)
            ent.set("Bueno")
        else:
            ent = ctk.CTkEntry(frame, width=300)
        ent.grid(row=i, column=1, padx=20, pady=15, sticky="w")
        entradas[campo] = ent

    def guardar():
        n = entradas["Nombre Completo"].get()
        try: ing = float(entradas["Ingresos Mensuales ($)"].get())
        except: messagebox.showerror("Error", "Ingresos numéricos requeridos"); return
        h = entradas["Historial Crediticio"].get()
        c = entradas["Datos de Contacto"].get()
        if not n or not c: messagebox.showwarning("Aviso", "Campos incompletos"); return
        if Reg_Clientes(n, ing, h, c).guardar():
            messagebox.showinfo("Éxito", "Cliente registrado")
            for e in entradas.values(): 
                if isinstance(e, ctk.CTkEntry): e.delete(0, tk.END)
        else: messagebox.showerror("Error", "Fallo en DB")

    ctk.CTkButton(frame, text="Guardar Cliente", fg_color=COLOR_BOTON_NORMAL, command=guardar).grid(row=4, column=0, columnspan=2, pady=20)

def vista_gestion_creditos(contenedor):
    limpiar_pantalla(contenedor)
    ctk.CTkLabel(contenedor, text="Gestión de Créditos", font=("Roboto", 24, "bold"), text_color=COLOR_TEXTO).pack(pady=(0, 20), anchor="w")
    
    f_t = ctk.CTkFrame(contenedor, fg_color=COLOR_FONDO_TARJETA)
    f_t.pack(fill="both", expand=True, padx=20, pady=10)
    
    cols = ("ID", "Cliente", "Monto", "Tasa", "Plazo", "Pago", "Estado")
    tabla = ttk.Treeview(f_t, columns=cols, show="headings")
    for c in cols: tabla.heading(c, text=c)
    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def ref():
        for r in tabla.get_children(): tabla.delete(r)
        df = Gestion_Creditos.obtener_todos()
        if not df.empty:
            for _, r in df.iterrows(): tabla.insert("", "end", values=(r['id'], r['nombre_cliente'], r['monto_otorgado'], r['tasa_interes'], r['plazo'], r['pago_mensual'], r['estado_actual']))
    ref()

    f_a = ctk.CTkFrame(contenedor, fg_color="transparent")
    f_a.pack(fill="x", padx=20)
    
    e_id = ctk.CTkEntry(f_a, placeholder_text="ID Cliente", width=80)
    e_id.pack(side="left", padx=5)
    e_m = ctk.CTkEntry(f_a, placeholder_text="Monto", width=80)
    e_m.pack(side="left", padx=5)
    e_t = ctk.CTkEntry(f_a, placeholder_text="Tasa", width=60)
    e_t.pack(side="left", padx=5)
    e_p = ctk.CTkEntry(f_a, placeholder_text="Meses", width=60)
    e_p.pack(side="left", padx=5)

    def apro():
        try:
            if Gestion_Creditos(int(e_id.get()), float(e_m.get()), float(e_t.get()), int(e_p.get())).guardar():
                messagebox.showinfo("OK", "Crédito Aprobado"); ref()
        except: messagebox.showerror("Error", "Datos inválidos")

    ctk.CTkButton(f_a, text="Aprobar", fg_color=COLOR_EXITO, command=apro).pack(side="left", padx=5)
    
    def est():
        s = tabla.selection()
        if not s: return
        ic = tabla.item(s[0])['values'][0]
        w = ctk.CTkToplevel(contenedor)
        w.geometry("150x150")
        for st in ["Activo", "Pagado", "En Mora"]:
            ctk.CTkButton(w, text=st, command=lambda x=st: [Gestion_Creditos.actualizar_estado(ic, x), ref(), w.destroy()]).pack(pady=2)

    ctk.CTkButton(f_a, text="Estado", command=est).pack(side="left", padx=5)

def vista_control_pagos(contenedor):
    limpiar_pantalla(contenedor)
    ctk.CTkLabel(contenedor, text="Pagos y Morosidad", font=("Roboto", 24, "bold"), text_color=COLOR_TEXTO).pack(pady=(0, 20), anchor="w")
    f = ctk.CTkFrame(contenedor, fg_color=COLOR_FONDO_TARJETA, corner_radius=15)
    f.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkLabel(f, text="ID Crédito:").grid(row=0, column=0, padx=20, pady=10)
    e_ic = ctk.CTkEntry(f)
    e_ic.grid(row=0, column=1, padx=20)
    
    ctk.CTkLabel(f, text="Monto:").grid(row=1, column=0, padx=20, pady=10)
    e_m = ctk.CTkEntry(f)
    e_m.grid(row=1, column=1, padx=20)
    
    ctk.CTkLabel(f, text="Días Retraso:").grid(row=2, column=0, padx=20, pady=10)
    e_d = ctk.CTkEntry(f)
    e_d.grid(row=2, column=1, padx=20)
    e_d.insert(0, "0")

    def pag():
        try:
            ic, m, d = int(e_ic.get()), float(e_m.get()), int(e_d.get())
            g = Control_Pagos(ic)
            mora = g.calcular_moratorios(m, d, 2.0)
            if mora > 0: messagebox.showwarning("Mora", f"Interés moratorio aplicado: ${mora}")
            if g.registrar_pago(m): messagebox.showinfo("Éxito", "Pago registrado")
        except: messagebox.showerror("Error", "Datos inválidos")

    ctk.CTkButton(f, text="Aplicar Pago", command=pag).grid(row=3, column=0, columnspan=2, pady=20)

def vista_busqueda_avanzada(contenedor):
    limpiar_pantalla(contenedor)
    ctk.CTkLabel(contenedor, text="Búsqueda y Buró", font=("Roboto", 24, "bold"), text_color=COLOR_TEXTO).pack(pady=(0, 20), anchor="w")
    f_b = ctk.CTkFrame(contenedor, fg_color="transparent")
    f_b.pack(fill="x", padx=20, pady=10)
    e = ctk.CTkEntry(f_b, placeholder_text="Buscar cliente...", width=300)
    e.pack(side="left", padx=5)
    
    f_r = ctk.CTkFrame(contenedor, fg_color=COLOR_FONDO_TARJETA)
    f_r.pack(fill="both", expand=True, padx=20, pady=10)
    t = ttk.Treeview(f_r, columns=("ID", "Nombre", "Ingresos", "Historial"), show="headings")
    for c in ("ID", "Nombre", "Ingresos", "Historial"): t.heading(c, text=c)
    t.pack(fill="both", expand=True, padx=10, pady=10)

    def bus():
        for r in t.get_children(): t.delete(r)
        df = Busqueda_Avanzada().buscar_por_nombre(e.get())
        for _, r in df.iterrows(): t.insert("", "end", values=(r['id'], r['nombre'], r['ingresos_mensuales'], r['historial_crediticio']))

    ctk.CTkButton(f_b, text="Buscar", command=bus).pack(side="left", padx=5)
    
    def buro():
        s = t.selection()
        if not s: return
        v = t.item(s[0])['values']
        res = Reg_Clientes.evaluar_buro(float(v[2]), v[3])
        messagebox.showinfo("Buró de Crédito", f"Cliente: {v[1]}\nResultado: {res}")

    ctk.CTkButton(f_b, text="Ver Buró", fg_color=COLOR_CUADRO_IMAGEN, text_color=COLOR_FONDO_PRINCIPAL, command=buro).pack(side="left", padx=5)

def vista_reportes_analisis(contenedor):
    limpiar_pantalla(contenedor)
    ctk.CTkLabel(contenedor, text="Reportes Analíticos", font=("Roboto", 24, "bold"), text_color=COLOR_TEXTO).pack(pady=(0, 20), anchor="w")
    f_g = ctk.CTkFrame(contenedor, fg_color=COLOR_FONDO_TARJETA)
    f_g.pack(fill="both", expand=True, padx=20, pady=10)
    
    plt_obj = Analisis_Datos.generar_grafico_dispersion()
    if plt_obj:
        canvas = FigureCanvasTkAgg(plt_obj, master=f_g)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    f_b = ctk.CTkFrame(contenedor, fg_color="transparent")
    f_b.pack(pady=10)
    def r1(): messagebox.showinfo("Reporte", f"Mora detectada en {len(Generacion_Reportes().obtener_creditos_en_mora())} créditos.")
    def r2(): messagebox.showinfo("Reporte", f"{len(Generacion_Reportes().clientes_elegibles_ampliacion())} clientes aptos para ampliación.")
    ctk.CTkButton(f_b, text="Créditos en Mora", command=r1).pack(side="left", padx=10)
    ctk.CTkButton(f_b, text="Elegibles Ampliación", command=r2).pack(side="left", padx=10)

def mostrar_menu_principal(v):
    limpiar_pantalla(v)
    v.geometry("1000x700")
    
    try:
        v_c = ctk.CTkToplevel(v)
        v_c.title("Sinox AI")
        v_c.geometry("400x600")
        v_c.attributes("-topmost", True)
        asistente = AplicacionChatbot(v_c)
    except: asistente = None

    sidebar = ctk.CTkFrame(v, width=200, fg_color=COLOR_FONDO_TARJETA)
    sidebar.pack(side="left", fill="y")
    ctk.CTkLabel(sidebar, text="BANK ADMIN", font=("Roboto", 20, "bold"), text_color=COLOR_TEXTO).pack(pady=20)

    cont = ctk.CTkFrame(v, fg_color=COLOR_FONDO_PRINCIPAL)
    cont.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def n(f, t):
        f(cont)
        if asistente and hasattr(asistente, 'actualizar_contexto'): asistente.actualizar_contexto(t)

    m = [("Clientes", vista_registro_clientes, "Registro"), ("Créditos", vista_gestion_creditos, "Créditos"), ("Pagos", vista_control_pagos, "Pagos"), ("Buró/Busq", vista_busqueda_avanzada, "Buró"), ("Análisis", vista_reportes_analisis, "Análisis")]
    for tx, fu, tn in m: ctk.CTkButton(sidebar, text=tx, fg_color="transparent", anchor="w", command=lambda f=fu, t=tn: n(f, t)).pack(fill="x", padx=10, pady=2)
    
    ctk.CTkButton(sidebar, text="Salir", fg_color=COLOR_ERROR, command=lambda: mostrar_pantalla_login(v)).pack(side="bottom", pady=20, padx=10, fill="x")
    n(vista_registro_clientes, "Registro")

def mostrar_pantalla_login(v):
    limpiar_pantalla(v); v.geometry("400x400")
    f = ctk.CTkFrame(v, fg_color=COLOR_FONDO_TARJETA, corner_radius=20)
    f.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    ctk.CTkLabel(f, text="ACCESO", font=("Roboto", 22, "bold")).pack(pady=20, padx=30)
    u = ctk.CTkEntry(f, placeholder_text="Usuario")
    u.pack(pady=10)
    p = ctk.CTkEntry(f, placeholder_text="Clave", show="*")
    p.pack(pady=10)
    ctk.CTkButton(f, text="Entrar", command=lambda: mostrar_menu_principal(v)).pack(pady=20)

def iniciar():
    v = ctk.CTk(); v.title("Bank System"); v.configure(fg_color=COLOR_FONDO_PRINCIPAL)
    mostrar_pantalla_login(v); v.mainloop()

if __name__ == "__main__": iniciar()