import requests
import logging
from app.models.pagos import Pagos

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PagosService:
    BASE_URL = "http://localhost:5001/procesar_pago"  # Cambia el puerto según corresponda

    @staticmethod
    def procesar_pago(producto_id, precio, medio_pago):
        # Validación de entrada
        if not isinstance(producto_id, int) or not isinstance(precio, (int, float)) or not isinstance(medio_pago, str):
            logger.error("Datos de entrada no válidos.")
            return None

        datos_pago = {
            "producto_id": producto_id,
            "precio": precio,
            "medio_pago": medio_pago,
        }

        try:
            respuesta = requests.post(PagosService.BASE_URL, json=datos_pago)

            if respuesta.status_code == 200:
                return Pagos.crear_pago(producto_id, precio, medio_pago)
            else:
                logger.error("Error al procesar el pago: %s", respuesta.json())
                return None

        except requests.exceptions.RequestException as e:
            logger.error("Error al conectar con el microservicio de pagos: %s", str(e))
            return None
