import unittest
from unittest.mock import patch
from app.services.pagos_service import PagosService
from app.models.pagos import Pagos
import requests

class TestPagosService(unittest.TestCase):
    pagos_service = PagosService

    @patch('requests.post')
    def test_procesar_pago_exitoso(self, mock_post):
        # Configuración del mock
        mock_post.return_value.status_code = 200

        # Simulación del método crear_pago
        mock_pago = Pagos(producto_id=1, precio=100, medio_pago="tarjeta")
        with patch.object(Pagos, 'crear_pago', return_value=mock_pago):
            resultado = self.pagos_service.procesar_pago(1, 100, "tarjeta")

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.producto_id, 1)
        self.assertEqual(resultado.medio_pago, "tarjeta")

    @patch('requests.post')
    def test_procesar_pago_fallo_pago(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.json = lambda: {"error": "Invalid payment"}

        resultado = self.pagos_service.procesar_pago(1, 100, "tarjeta")

        self.assertIsNone(resultado)

    @patch('requests.post')
    def test_procesar_pago_error_conexion(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Error de conexión")

        resultado = self.pagos_service.procesar_pago(1, 100, "tarjeta")

        self.assertIsNone(resultado)

    def test_procesar_pago_invalid_input(self):
        resultado = self.pagos_service.procesar_pago("invalid_id", "invalid_amount", 100)
        self.assertIsNone(resultado)

if __name__ == "__main__":
    unittest.main()
