import customtkinter as ctk
from P_OO import *
from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import shutil
import os
from datetime import datetime, timedelta

from supabase import create_client, Client
# pip install supabase

# Reemplaza estos valores con la URL y Key (anon public) de tu proyecto en Supabase
SUPABASE_URL = "https://jvrarglskymgrjfvgyuy.supabase.co"
SUPABASE_KEY = "sb_publishable_FIaH2NGVgIUNI0UuLU6d6A_tbyIRe-6"

#-----------------------------------------------------------------------

COLOR_FONDO_PRINCIPAL = "#ba8445"
COLOR_BOTON_AZUL_REY = "#c1876b"
COLOR_BOTON_HOVER = "#b9935a"
COLOR_CUADRO_IMAGEN = "#bc8e47"

def limpiar_pantalla(ventana):
    """Elimina todos los widgets de la ventana actual."""
    for widget in ventana.winfo_children():
        widget.destroy()

def _crear_boton_cerrar_sesion(ventana):
    """Crea el botón para regresar al login."""
    btn_cerrar = ctk.CTkButton(
        ventana, 
        text="Cerrar Sesión", 
        fg_color="#dc2626", 
        hover_color="#3c0ed3",
        font=("Roboto", 14, "bold"),
        command=lambda: mostrar_pantalla_login(ventana)
    )
    btn_cerrar.pack(pady=20)

def mostrar_pantalla_login(ventana):
    limpiar_pantalla(ventana)
    ventana.title("NA - Iniciar Sesión")

    frame_login = ctk.CTkFrame(ventana, corner_radius=20, fg_color="#8f8b66")
    frame_login.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    label_titulo = ctk.CTkLabel(frame_login, text="Lorem Ipsum", font=("Roboto", 24, "bold"), text_color="white")
    label_titulo.pack(pady=(30, 10), padx=40)

    frame_imagen = ctk.CTkFrame(frame_login, width=300, height=150, fg_color=COLOR_CUADRO_IMAGEN, corner_radius=10)
    frame_imagen.pack(pady=10)

    entry_usuario = ctk.CTkEntry(frame_login, placeholder_text="Nombre de usuario", width=250, height=40, corner_radius=10)
    entry_usuario.pack(pady=10)

    entry_password = ctk.CTkEntry(frame_login, placeholder_text="Contraseña", show="*", width=250, height=40, corner_radius=10)
    entry_password.pack(pady=10)

    label_error = ctk.CTkLabel(frame_login, text="", text_color="#ef4444", font=("Roboto", 12))
    label_error.pack(pady=5)

def iniciar_aplicacion():
    ventana = ctk.CTk()
    ventana.geometry("600x600")
    ventana.configure(fg_color=COLOR_FONDO_PRINCIPAL)
    ventana.title("Cargando Sistema...")
    mostrar_pantalla_login(ventana)
    
    ventana.mainloop()

iniciar_aplicacion()