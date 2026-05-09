import os
from supabase import create_client, Client
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            url: str = os.environ.get("SUPABASE_URL", "https://jvrarglskymgrjfvgyuy.supabase.co")
            key: str = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp2cmFyZ2xza3ltZ3JqZnZneXV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMwNjIxNzEsImV4cCI6MjA4ODYzODE3MX0.3XyF3q13M_zJ_MLQfxfvOncGTpnEaMHDmmFfY1-RFWk")
            try:
                cls._instance.client: Client = create_client(url, key)
            except Exception as e:
                cls._instance.client = None
        return cls._instance

class Reg_Clientes:
    def __init__(self, nombre: str, ingresos_mensuales: float, historial_crediticio: str, datos_contacto: str, id_cliente: int = None):
        self._id_cliente = id_cliente
        self.nombre = nombre 
        self.ingresos_mensuales = ingresos_mensuales 
        self.historial_crediticio = historial_crediticio 
        self.datos_contacto = datos_contacto 
        self.db = DatabaseConnection().client

    def guardar(self):
        if not self.db: return False
        data = {"nombre": self.nombre, "ingresos_mensuales": self.ingresos_mensuales, "historial_crediticio": self.historial_crediticio, "datos_contacto": self.datos_contacto}
        try:
            response = self.db.table("clientes").insert(data).execute()
            self._id_cliente = response.data[0]['id']
            return True
        except Exception: return False

    @staticmethod
    def obtener_todos():
        db = DatabaseConnection().client
        if not db: return pd.DataFrame()
        try:
            all_data = []
            offset, limit = 0, 1000
            while True:
                response = db.table("clientes").select("*").range(offset, offset + limit - 1).execute()
                if not response.data: break
                all_data.extend(response.data)
                if len(response.data) < limit: break
                offset += limit
            return pd.DataFrame(all_data)
        except Exception: return pd.DataFrame()

    @staticmethod
    def evaluar_buro(ingresos, historial):
        puntos = 0
        if historial == "Excelente": puntos += 50
        elif historial == "Bueno": puntos += 30
        elif historial == "Regular": puntos += 10
        
        if ingresos > 20000: puntos += 50
        elif ingresos > 10000: puntos += 30
        elif ingresos > 5000: puntos += 10
        
        if puntos >= 80: return "Apto - Riesgo Bajo"
        if puntos >= 40: return "Apto - Riesgo Medio"
        return "No Apto - Riesgo Alto"

class Gestion_Creditos:
    def __init__(self, cliente_id: int, monto_otorgado: float, tasa_interes: float, plazo: int, estado_actual: str = "Activo", id_credito: int = None):
        self._id_credito = id_credito
        self.id_cliente = cliente_id
        self.monto_otorgado = monto_otorgado 
        self.tasa_interes = tasa_interes 
        self.plazo = plazo 
        self.estado_actual = estado_actual
        self.pago_mensual = self.calcular_pago_mensual() 
        self.db = DatabaseConnection().client

    def calcular_pago_mensual(self) -> float:
        if self.tasa_interes == 0: return self.monto_otorgado / self.plazo
        tasa_mensual = self.tasa_interes / 12 / 100
        num = self.monto_otorgado * tasa_mensual * ((1 + tasa_mensual) ** self.plazo)
        den = ((1 + tasa_mensual) ** self.plazo) - 1
        return round(num / den, 2)

    def guardar(self):
        if not self.db: return False
        data = {"cliente_id": self.id_cliente, "monto_otorgado": self.monto_otorgado, "tasa_interes": self.tasa_interes, "plazo": self.plazo, "pago_mensual": self.pago_mensual, "estado_actual": self.estado_actual}
        try:
            response = self.db.table("creditos").insert(data).execute()
            self._id_credito = response.data[0]['id']
            return True
        except Exception: return False

    @staticmethod
    def obtener_todos():
        db = DatabaseConnection().client
        if not db: return pd.DataFrame()
        try:
            all_data = []
            offset, limit = 0, 1000
            while True:
                response = db.table("creditos").select("*, clientes(nombre)").range(offset, offset + limit - 1).execute()
                if not response.data: break
                all_data.extend(response.data)
                if len(response.data) < limit: break
                offset += limit
            data = []
            for item in all_data:
                row = item.copy()
                row['nombre_cliente'] = item['clientes']['nombre'] if item.get('clientes') else 'N/A'
                del row['clientes']
                data.append(row)
            return pd.DataFrame(data)
        except Exception: return pd.DataFrame()

    @staticmethod
    def actualizar_estado(id_credito: int, nuevo_estado: str):
        db = DatabaseConnection().client
        if not db: return False
        try:
            db.table("creditos").update({"estado_actual": nuevo_estado}).eq("id", id_credito).execute()
            return True
        except Exception: return False

class Control_Pagos:
    def __init__(self, credito_id: int):
        self.credito_id = credito_id
        self.db = DatabaseConnection().client

    def registrar_pago(self, monto: float, fecha: str = None):
        if fecha is None: fecha = datetime.now().strftime("%Y-%m-%d")
        if self.db:
            data = {"credito_id": self.credito_id, "fecha_pago": fecha, "monto_abonado": monto}
            try: self.db.table("pagos").insert(data).execute(); return True
            except Exception: return False
        return False

    def calcular_moratorios(self, monto_base: float, dias_retraso: int, tasa_penalizacion: float) -> float:
        penalizacion = 0.0
        if dias_retraso > 0: penalizacion = monto_base * (tasa_penalizacion / 100) * dias_retraso
        return round(penalizacion, 2)

class Busqueda_Avanzada:
    def __init__(self):
        self.db = DatabaseConnection().client

    def buscar_por_nombre(self, nombre_cliente: str): 
        df_clientes = Reg_Clientes.obtener_todos()
        if df_clientes.empty: return pd.DataFrame()
        return df_clientes[df_clientes['nombre'].str.contains(nombre_cliente, case=False, na=False)]

    def buscar_por_estado_credito(self, estado: str): 
        if not self.db: return pd.DataFrame()
        try:
            response = self.db.table("creditos").select("*, clientes(nombre)").eq("estado_actual", estado).execute()
            data = []
            for item in response.data:
                row = item.copy()
                row['nombre_cliente'] = item['clientes']['nombre'] if item.get('clientes') else 'N/A'
                del row['clientes']
                data.append(row)
            return pd.DataFrame(data)
        except Exception: return pd.DataFrame()

class Generacion_Reportes:
    def __init__(self):
        self.db = DatabaseConnection().client

    def obtener_creditos_en_mora(self): 
        if not self.db: return pd.DataFrame()
        try:
            response = self.db.table("creditos").select("*, clientes(nombre)").eq("estado_actual", "En Mora").execute()
            data = []
            for item in response.data:
                row = item.copy()
                row['nombre_cliente'] = item['clientes']['nombre'] if item.get('clientes') else 'N/A'
                del row['clientes']
                data.append(row)
            return pd.DataFrame(data)
        except Exception: return pd.DataFrame()

    def clientes_elegibles_ampliacion(self): 
        if not self.db: return pd.DataFrame()
        try:
            response = self.db.table("clientes").select("*").gte("ingresos_mensuales", 15000).execute()
            return pd.DataFrame(response.data)
        except Exception: return pd.DataFrame()

class Analisis_Datos:
    @staticmethod
    def generar_grafico_dispersion(): 
        df_clientes = Reg_Clientes.obtener_todos()
        db = DatabaseConnection().client
        if df_clientes.empty or not db: return None
        try:
            all_creditos = []
            offset, limit = 0, 1000
            while True:
                res = db.table("creditos").select("*").range(offset, offset + limit - 1).execute()
                if not res.data: break
                all_creditos.extend(res.data)
                if len(res.data) < limit: break
                offset += limit
            df_creditos = pd.DataFrame(all_creditos)
            if df_creditos.empty: return None
            df_completo = pd.merge(df_clientes, df_creditos, left_on='id', right_on='cliente_id')
            fig = plt.figure(figsize=(6, 4))
            plt.scatter(df_completo['ingresos_mensuales'], df_completo['monto_otorgado'], alpha=0.6, color='#5884b0')
            plt.title('Ingresos vs Montos Otorgados')
            plt.xlabel('Ingresos ($)')
            plt.ylabel('Monto Crédito ($)')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            return fig
        except Exception: return None
