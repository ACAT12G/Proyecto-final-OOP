import tkinter as tk
import customtkinter as ctk
from openai import OpenAI
from PIL import Image
import os
import copy 
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

ctk.set_appearance_mode("dark") 

prompt = '''
<background info>
Funcionalidades del sistema:
Registro de los clientes: Registrar a los clientes con datos como su nombre; ingresos mensuales; historial crediticio y datos de contacto. Cabe recalcar que estos datos serán censurados y no hechos públicos para mantener el anonimato del cliente.
Gestión de créditos: Una sección que permite al empleado gestionar y visualizar el monto otorgado, tasa de interés, plazo, pago mensual y estado actual de crédito de los clientes.
Control de pagos: Da al empleado la capacidad de visualizar los registros de fechas de pago y montos abonados; además de también poder calcular los intereses moratorios. 
Búsqueda avanzada: Función de búsqueda que deja al empleado buscar a un cliente de manera específica por uno o más de los siguientes datos: por nombre de cliente, estado del crédito o fechas de vencimiento.
Generación de reportes: Una función que permite al empleado generar reportes que pueden contener uno de los siguientes tipos de datos:
Créditos en mora o con riesgo de impago.
Tipos de crédito más solicitados y rentables.
Clientes elegibles para ampliación de línea de crédito.
Análisis de datos: Una función que permite ver los datos de una manera mucho más gráfica y sin publicar o vulnerar los datos explícitos de clientes individuales. La función permite generar y visualizar:
Gráficos de dispersión relacionando ingresos vs. probabilidad de impago.
Tendencias de ingresos por cobro de intereses a lo largo del año.

Límites o restricciones del proyecto:
Tiempo: Las funciones que buscamos realizar están subyugadas por el tiempo que se dispone para crearlas, y, por ende, su alcance y estabilidad final no se puede aseverar por completo. 
Capacidades del servidor: Debido a que se está usando “Supabase” para cargar y obtener los datos de los clientes, se depende este mismo para delimitar la cantidad de clientes que se puede tener, y de querer mejorar la calidad se tendría que realizar una inversión. 
Límites naturales: El sistema está limitado a seguir solo ciertos tipos de datos a modo de input, y dar otros como output, si se quisiera modificar o cambiar alguno de los dos para cumplir otras funciones, se requeriría un cambio completo o parcial en el código completo. Cambios futuros: Hay que tener en cuenta que la economía y los sistemas de este tipo cambian con el tiempo, lo que indica que es probable que en cierta extensión de tiempo este código quede faltante de funciones requeridas en el estado de la economía que se pueda tener en un futuro. 
Límites legales: Aquellos limites que, según las leyes jurídicas, ponen ciertas reglas específicas que se deben seguir para que sea aplicable en entornos reales sin ningún tipo de problema jurídico

Requerimientos del sistema:
Activos:
Registro de clientes.
Gestión de créditos, junto a sus estados y cantidades.
Control de pagos y datos relacionados.
Búsqueda avanzada intuitiva y accesible por palabras clave.
Generación de reportes con datos específicos y diversos.
Análisis de datos y visualización de los datos.
Revisar el buro de crédito.
Pasivos:
Uso: Interfaz intuitiva fácil de aprender y manipular y amigable a los ojos.
Graficas: Gráficas y visualizaciones de datos adaptativas en tiempo real según
los datos presentes en la base.
Datos en la nube: Base de datos en “Supabase”; datos en la nube que están
disponibles en cualquier dispositivo que se pueden manipular desde la
interfaz gráfica.
Output del programa: Output de la generación de reportes que puede usado
para más funciones y fácil de crear en la interfaz.
Anonimidad: Los datos de los clientes no son filtrados en ningún tipo de output de carácter público o visualización.
</background info>

<role>
You are 'Sinox AI' or just 'Sinox' for short; a modern, educated and formal assistant with years of experience in bank systems and economy; you are educated, sharp and to the point. You don't like asking questions and prefer to focus on what the user needs to know and nothing more.
</role>

<jail>
You will adhere by natural and rational ethical protocols; avoid any NSFW acts at all costs.
End the conversation if any risque topics were to arise.
</jail>

<app_map>
Conoces la estructura del sistema bancario. Estas son las pantallas existentes:
- Login: Acceso al sistema.
- Registro de Clientes: Captura Nombre, Ingresos, Historial Crediticio y Contacto.
- Gestión de Créditos: Muestra tabla de créditos, permite Aprobar Nuevo y Actualizar Estado.
- Control de Pagos: Pide ID de Crédito y Monto a Abonar. Calcula intereses moratorios.
- Búsqueda Avanzada: Búsqueda por palabras clave (nombre, fecha, estado).
- Reportes y Análisis: Gráficos de Ingresos vs Riesgo y exportación a PDF/Excel.
</app_map>

<objective>
Your objetive will be to help the user understand and control the bank app you're an assistant of. 
You need to avoid confusion or errors, and focus on helping user reach their objetive as fast and clean as you can.
</objective>

<format>
You will always answer in text; using a modern and formal lenguage, avoid the use of advanced and complex terms.
Don't write wordy or extensive answers and focus on being as clear as possible.
No emojis.
No games.
No overstimulation or crudish / informal lenguage.
</format>

<greeting>
(This is the starting message the {{user}} will act upon, don't focus on it after the first message.)
Hello, I am your assistant. Do you have any questions? 
</greeting>
'''

greeting = '''
Remember, all answers are made by AI and don't represent the opinions of the provider / Recuerda, esto es IA, y sus respuestas no representan la opinion de proveedor.'''

greetinges = '''
Hola, soy tu asistente. ¿Tienes alguna pregunta?
'''

greetingen = '''
Hello, I am your assistant. Do you have any questions? 
'''

class AplicacionChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Sinox AI")
        self.root.geometry("900x650")
        self.pantalla_actual_usuario = "Login"
        
        # Color Base Profundo
        self.root.configure(fg_color="#030a21")

        llave = os.getenv("SINOX_API_KEY")
        
        # ==========================================
        # EL ESCUDO DE SEGURIDAD (FIX PANTALLA BLANCA)
        # ==========================================
        if not llave:
            print("⚠️ ALERTA: No se encontró el archivo .env o la variable SINOX_API_KEY. Usando modo de emergencia.")
            llave = "LLAVE_NO_ENCONTRADA_O_INVALIDA" # Esto evita que Python colapse.
            
        self.client = OpenAI(
            base_url="https://api.meganova.ai/v1",
            api_key=llave
        )
        
        try:
            self.img_sinox_pasiva = ctk.CTkImage(
                light_image=Image.open("sinox.png"), 
                dark_image=Image.open("sinox.png"), 
                size=(80, 80) 
            )
            self.img_sinox_activa = ctk.CTkImage(
                light_image=Image.open("sinox1.png"), 
                dark_image=Image.open("sinox1.png"), 
                size=(80, 80)
            )
        except Exception as e:
            print(f"Atención: No se encontraron las imágenes de Sinox. Usando emojis. Detalle: {e}")
            self.img_sinox_pasiva = None
            self.img_sinox_activa = None
        # =========================================================

        self.chat_history = []
        self.frame_actual = None
        self.greeting_actual = "" 
        
        self.mostrar_pantalla_bienvenida()

    def cambiar_pantalla(self, nuevo_frame):
        if self.frame_actual is not None:
            self.frame_actual.destroy()
        self.frame_actual = nuevo_frame
        self.frame_actual.pack(expand=True, fill="both", padx=20, pady=20)

    def mostrar_pantalla_bienvenida(self):
        frame_bienvenida = ctk.CTkFrame(self.root, fg_color="#042b62", corner_radius=15)
        
        ctk.CTkLabel(frame_bienvenida, text="¡Hola! Este es Sinox AI", 
                     font=ctk.CTkFont(size=28, weight="bold"), text_color="white").pack(pady=(80, 10))
        ctk.CTkLabel(frame_bienvenida, text="Select your language / Seleccione su idioma:", 
                     font=ctk.CTkFont(size=14), text_color="#c8eaff").pack(pady=(0, 40))
        
        btn_es = ctk.CTkButton(frame_bienvenida, text="Español", 
                               fg_color="#5884b0", hover_color="#7da1c3", text_color="white",
                               font=ctk.CTkFont(size=14, weight="bold"), height=40,
                               command=lambda: self.iniciar_chat("es"))
        btn_es.pack(pady=10)
        
        btn_en = ctk.CTkButton(frame_bienvenida, text="English", 
                               fg_color="#5884b0", hover_color="#7da1c3", text_color="white",
                               font=ctk.CTkFont(size=14, weight="bold"), height=40,
                               command=lambda: self.iniciar_chat("en"))
        btn_en.pack(pady=10)
        
        self.cambiar_pantalla(frame_bienvenida)

    def iniciar_chat(self, idioma):
        if idioma == "es":
            prompt_final = prompt + "\n\n<language_rule>\nCRITICAL: You must ALWAYS respond in Spanish.\n</language_rule>"
            self.greeting_actual = greeting + greetinges
        else:
            prompt_final = prompt + "\n\n<language_rule>\nCRITICAL: You must ALWAYS respond in English.\n</language_rule>"
            self.greeting_actual = greeting + greetingen

        self.chat_history = [{"role": "system", "content": prompt_final}]
        self.mostrar_pantalla_chat()

    def _mascota_hablando(self):
        if self.img_sinox_activa:
            self.mascota_label.configure(image=self.img_sinox_activa, text="")
        else:
            self.mascota_label.configure(text="😮") 
        self.root.update()

    def _mascota_callada(self):
        if self.img_sinox_pasiva:
            self.mascota_label.configure(image=self.img_sinox_pasiva, text="")
        else:
            self.mascota_label.configure(text="😐") 
        self.root.update()

    def mostrar_pantalla_chat(self):
        frame_chat = ctk.CTkFrame(self.root, fg_color="#030a21") 
        
        barra_herramientas = ctk.CTkFrame(frame_chat, fg_color="transparent")
        barra_herramientas.pack(fill=tk.X, pady=5)
        
        btn_reload = ctk.CTkButton(barra_herramientas, text="♻️ Reload", width=100,
                                   fg_color="#5884b0", hover_color="#7da1c3", text_color="white",
                                   font=ctk.CTkFont(weight="bold"), command=self.recargar_respuesta)
        btn_reload.pack(side=tk.RIGHT, padx=5)
        
        btn_edit = ctk.CTkButton(barra_herramientas, text="✏️ Edit", width=100,
                                 fg_color="#5884b0", hover_color="#7da1c3", text_color="white",
                                 font=ctk.CTkFont(weight="bold"), command=self.editar_mensaje)
        btn_edit.pack(side=tk.RIGHT, padx=5)
        
        # --- Área de la Mascota ---
        if self.img_sinox_pasiva:
            self.mascota_label = ctk.CTkLabel(frame_chat, text="", image=self.img_sinox_pasiva)
        else:
            self.mascota_label = ctk.CTkLabel(frame_chat, text="😐", font=ctk.CTkFont(size=50))
        self.mascota_label.pack(pady=5)
        
        # --- Visor de Chat ---
        self.chat_display = ctk.CTkTextbox(frame_chat, font=ctk.CTkFont(size=14), 
                                           fg_color="#042b62", text_color="white", 
                                           corner_radius=10, border_width=2, border_color="#5f8ebd")
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.chat_display.tag_config("user_name", foreground="#c8eaff")
        self.chat_display.tag_config("ai_name", foreground="#c8eaff")
        self.chat_display.tag_config("text_body", foreground="white")
        self.chat_display.tag_config("error", foreground="#ff6b6b")
        
        # --- Área de entrada y envío ---
        input_frame = ctk.CTkFrame(frame_chat, fg_color="transparent")
        input_frame.pack(fill=tk.X, pady=5)
        
        self.input_box = ctk.CTkEntry(input_frame, font=ctk.CTkFont(size=14), 
                                      fg_color="#042b62", text_color="white",
                                      border_color="#5884b0", border_width=2, corner_radius=10)
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        submit_button = ctk.CTkButton(input_frame, text="Send!", width=100, height=35,
                                      fg_color="#5884b0", hover_color="#7da1c3", text_color="white",
                                      font=ctk.CTkFont(size=14, weight="bold"), command=self.update_output)
        submit_button.pack(side=tk.RIGHT)
        
        self.cambiar_pantalla(frame_chat)
        self._refrescar_pantalla_chat()

    def _refrescar_pantalla_chat(self):
        self.chat_display.configure(state="normal") 
        self.chat_display.delete("1.0", tk.END)   
        
        self.chat_display.insert(tk.END, "Sinox AI:\n", "ai_name")
        self.chat_display.insert(tk.END, f"{self.greeting_actual}\n\n", "text_body")
        
        for msg in self.chat_history:
            if msg["role"] == "system": 
                continue 
            elif msg["role"] == "user":
                self.chat_display.insert(tk.END, "Tú:\n", "user_name")
                self.chat_display.insert(tk.END, f"{msg['content']}\n\n", "text_body")
            elif msg["role"] == "assistant":
                self.chat_display.insert(tk.END, "Sinox AI:\n", "ai_name")
                self.chat_display.insert(tk.END, f"{msg['content']}\n\n", "text_body")
        
        self.chat_display.see(tk.END) 
        self.chat_display.configure(state="disabled") 
        self.root.update()

    def update_output(self):
        user_prompt = self.input_box.get()
        if not user_prompt: return 
        
        self.chat_history.append({"role": "user", "content": user_prompt})
        self.input_box.delete(0, tk.END) 
        
        self._refrescar_pantalla_chat()
        self._generar_respuesta_api()

    def editar_mensaje(self):
        if len(self.chat_history) >= 3:
            self.chat_history.pop() 
            ultimo_prompt = self.chat_history.pop()["content"] 
            
            self.input_box.delete(0, tk.END)
            self.input_box.insert(0, ultimo_prompt)
            self._refrescar_pantalla_chat()

    def recargar_respuesta(self):
        if len(self.chat_history) >= 3:
            self.chat_history.pop() 
            self._refrescar_pantalla_chat() 
            self._generar_respuesta_api() 

    def actualizar_contexto(self, nueva_pantalla):
        self.pantalla_actual_usuario = nueva_pantalla

    def _generar_respuesta_api(self):
        self.chat_display.configure(state="normal")
        self.chat_display.insert(tk.END, "Sinox AI (Escribiendo...):\n", "ai_name")
        self.root.update()

        try:
            self._mascota_hablando()
            
            # EL TRUCO MAESTRO LIMPIO (Sin código duplicado)
            historial_con_contexto = copy.deepcopy(self.chat_history)
            mensaje_gps = f"\n\n[INFO INTERNA DEL SISTEMA: El usuario está viendo la pantalla '{self.pantalla_actual_usuario}'. Basa tu respuesta en esta pantalla.]"
            historial_con_contexto[-1]["content"] += mensaje_gps

            response = self.client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3-0324-Free",
                messages=historial_con_contexto,
                max_tokens=None,
                temperature=0.7,
                stream=True
            )
            
            ai_response = ""
            self.chat_display.delete("end-2l", "end-1c") 
            self.chat_display.insert(tk.END, "Sinox AI:\n", "ai_name")
            
            for chunk in response:
                fragmento = chunk.choices[0].delta.content
                if fragmento is not None:
                    ai_response += fragmento
                    self.chat_display.insert(tk.END, fragmento, "text_body") 
                    self.chat_display.see(tk.END)
                    self.root.update()
            
            self.chat_display.insert(tk.END, "\n\n")
            self.chat_history.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            # Si el .env falló, este error te lo dirá claramente en el chat de la IA
            self.chat_display.insert(tk.END, f"[Error de conexión con OpenAI: {e}]\n\n", "error")
            self.chat_history.pop()
            
        finally:
            self._mascota_callada()
            self.chat_display.configure(state="disabled")

if __name__ == "__main__":
    ventana_principal = ctk.CTk() 
    app = AplicacionChatbot(ventana_principal)
    ventana_principal.mainloop()