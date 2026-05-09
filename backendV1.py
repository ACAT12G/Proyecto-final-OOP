import os
from supabase import create_client, Client
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# CONEXIÓN A BASE DE DATOS
class DatabaseConnection:
    #Clase Singleton para manejar la conexión a Supabase
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            # Reemplaza con tus credenciales de Supabase
            url: str = os.environ.get("SUPABASE_URL", "https://jvrarglskymgrjfvgyuy.supabase.co")
            key: str = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp2cmFyZ2xza3ltZ3JqZnZneXV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMwNjIxNzEsImV4cCI6MjA4ODYzODE3MX0.3XyF3q13M_zJ_MLQfxfvOncGTpnEaMHDmmFfY1-RFWk")
            try:
                cls._instance.client: Client = create_client(url, key)
            except Exception as e:
                print(f"Error al conectar con Supabase: {e}")
                cls._instance.client = None
        return cls._instance

# MODELOS DE DATOS 
class Reg_Clientes:
    #Clase que maneja el registro y datos de los clientes
    def __init__(self, nombre: str, ingresos_mensuales: float, historial_crediticio: str, datos_contacto: str, id_cliente: int = None):
        self._id_cliente = id_cliente
        self.nombre = nombre 
        self.ingresos_mensuales = ingresos_mensuales 
        self.historial_crediticio = historial_crediticio 
        self.datos_contacto = datos_contacto 
        self.db = DatabaseConnection().client

    def guardar(self):
        #Guarda el registro del cliente en la base de datos Supabase
        if not self.db: return False
        data = {
            "nombre": self.nombre,
            "ingresos_mensuales": self.ingresos_mensuales,
            "historial_crediticio": self.historial_crediticio,
            "datos_contacto": self.datos_contacto
        }
        try:
            response = self.db.table("clientes").insert(data).execute()
            self._id_cliente = response.data[0]['id']
            return True
        except Exception as e:
            print(f"Error al guardar cliente: {e}")
            return False

    @staticmethod
    def obtener_todos():
        #Retorna un DataFrame de Pandas con todos los clientes
        db = DatabaseConnection().client
        if not db: return pd.DataFrame()
        response = db.table("clientes").select("*").execute()
        return pd.DataFrame(response.data)


class Gestion_Creditos:
    #Clase para administrar los detalles de los créditos otorgados
    
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
        #Calcula el pago mensual utilizando la fórmula de amortización estándar
        
        if self.tasa_interes == 0:
            return self.monto_otorgado / self.plazo
        
        tasa_mensual = self.tasa_interes / 12 / 100
        numerador = self.monto_otorgado * tasa_mensual * ((1 + tasa_mensual) ** self.plazo)
        denominador = ((1 + tasa_mensual) ** self.plazo) - 1
        return round(numerador / denominador, 2)

    def guardar(self):
        #Guarda el crédito en Supabase
        if not self.db: return False
        data = {
            "cliente_id": self.id_cliente,
            "monto_otorgado": self.monto_otorgado,
            "tasa_interes": self.tasa_interes,
            "plazo": self.plazo,
            "pago_mensual": self.pago_mensual,
            "estado_actual": self.estado_actual
        }
        try:
            response = self.db.table("creditos").insert(data).execute()
            self._id_credito = response.data[0]['id']
            return True
        except Exception as e:
            print(f"Error al guardar crédito: {e}")
            return False


class Control_Pagos:
        #Clase para registrar pagos y calcular intereses moratorios
    
    def __init__(self, credito_id: int):
        self.credito_id = credito_id
        self.fechas_pago = [] 
        self.montos_abonados = [] 
        self.intereses_moratorios = 0.0 
        self.db = DatabaseConnection().client

    def registrar_pago(self, monto: float, fecha: str = None):
        """Registra un nuevo abono y lo sube a la base de datos."""
        if fecha is None:
            fecha = datetime.now().strftime("%Y-%m-%d")
            
        self.fechas_pago.append(fecha)
        self.montos_abonados.append(monto)
        
        if self.db:
            data = {"credito_id": self.credito_id, "fecha_pago": fecha, "monto_abonado": monto}
            self.db.table("pagos").insert(data).execute()

    def calcular_moratorios(self, dias_retraso: int, tasa_penalizacion: float) -> float:
        #Calcula los intereses generados por retraso mediante lógica secuencial básica.
        penalizacion = 0.0
        if dias_retraso > 0:
            penalizacion = (self.montos_abonados[-1] if self.montos_abonados else 0) * (tasa_penalizacion / 100) * dias_retraso
        self.intereses_moratorios += penalizacion
        return penalizacion

# SERVICIOS Y ANÁLISIS
class Busqueda_Avanzada:
    #Clase para ejecutar consultas y filtros sobre la base de datos
    
    def __init__(self):
        self.db = DatabaseConnection().client

    def buscar_por_nombre(self, nombre_cliente: str): 
        """Busca clientes utilizando coincidencia de texto."""
        df_clientes = Reg_Clientes.obtener_todos()
        if df_clientes.empty: return pd.DataFrame()
        # Filtro utilizando Pandas
        resultados = df_clientes[df_clientes['nombre'].str.contains(nombre_cliente, case=False, na=False)]
        return resultados

    def buscar_por_estado_credito(self, estado_credito: str): 
        """Retorna créditos filtrados por estado (Activo, Pagado, En Mora)."""
        if not self.db: return pd.DataFrame()
        response = self.db.table("creditos").select("*").eq("estado_actual", estado_credito).execute()
        return pd.DataFrame(response.data)


class Generacion_Reportes:
    #Clase encargada de estructurar datos para la toma de decisiones
    
    def __init__(self):
        self.db = DatabaseConnection().client

    def obtener_creditos_en_mora(self) -> list: 
        if not self.db: return []
        response = self.db.table("creditos").select("*, clientes(nombre)").eq("estado_actual", "En Mora").execute()
        return response.data

    def clientes_elegibles_ampliacion(self) -> list: 
        #Lógica: Clientes con ingresos altos y créditos pagados puntualmente
        if not self.db: return []
        response = self.db.table("clientes").select("*").gte("ingresos_mensuales", 15000).execute()
        return response.data


class Analisis_Datos:
    #Clase dedicada a la visualización analítica de los datos
    
    @staticmethod
    def generar_grafico_dispersion(): 
        #Genera un gráfico de dispersión: Ingresos vs Monto Otorgado
        df_clientes = Reg_Clientes.obtener_todos()
        db = DatabaseConnection().client
        
        if df_clientes.empty or not db: return None
        
        res_creditos = db.table("creditos").select("*").execute()
        df_creditos = pd.DataFrame(res_creditos.data)
        
        if df_creditos.empty: return None

        # Unir DataFrames por ID de cliente utilizando Pandas
        df_completo = pd.merge(df_clientes, df_creditos, left_on='id', right_on='cliente_id')
        
        plt.figure(figsize=(8, 6))
        plt.scatter(df_completo['ingresos_mensuales'], df_completo['monto_otorgado'], alpha=0.6, color='blue')
        plt.title('Dispersión: Ingresos Mensuales vs Montos Otorgados')
        plt.xlabel('Ingresos Mensuales ($)')
        plt.ylabel('Monto del Crédito ($)')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        return True