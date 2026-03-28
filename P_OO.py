class Reg_Clientes:
    def __init__(self, Nombre, ingresos_mensuales, historial_crediticio, datos_contacto):
        self.nombre = Nombre
        self.ingresos_mensuales = ingresos_mensuales
        self.historial_crediticio = historial_crediticio
        self.datos_contacto = datos_contacto

class Gestion_Creditos:
    def __init__(self, monto_otorgado, tasa_interes, plazo, pago_mensual, estado_actual_credito):
        self.monto_otorgado = monto_otorgado
        self.tasa_interes = tasa_interes
        self.plazo = plazo
        self.pago_mensual = pago_mensual
        self.estado_actual_credito = estado_actual_credito

class Control_Pagos:
    def __init__(self, fechas_pago, montos_abonados, intereses_moratorios):
        self.fechas_pago = fechas_pago
        self.montos_abonados = montos_abonados
        self.intereses_moratorios = intereses_moratorios

class Busqueda_Avanzada:
    def __init__(self, nombre_cliente, estado_credito, fechas_vencimiento):
        self.nombre_cliente = nombre_cliente
        self.estado_credito = estado_credito
        self.fechas_vencimiento = fechas_vencimiento

class Generacion_Reportes:
    def __init__(self, creditos_en_mora, tipos_credito_rentables, clientes_elegibles_ampliacion):
        self.creditos_en_mora = creditos_en_mora
        self.tipos_credito_rentables = tipos_credito_rentables
        self.clientes_elegibles_ampliacion = clientes_elegibles_ampliacion

class Analisis_Datos:
    def __init__(self, graficos_dispersion, tendencia_ingresos):
        self.graficos_dispersion = graficos_dispersion
        self.tendencia_ingresos = tendencia_ingresos