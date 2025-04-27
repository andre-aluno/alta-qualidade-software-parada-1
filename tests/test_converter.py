import unittest
import os
import sys
from decimal import Decimal, ROUND_HALF_UP
import io
from contextlib import redirect_stderr

# Ajustar o path para importar o módulo converter
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import converter

class TestConversorMoedas(unittest.TestCase):
    def setUp(self):
        # Taxas fixas para os testes
        self.taxas = {
            "USD": {"EUR": 0.92, "BRL": 5.20},
            "EUR": {"USD": 1.09, "BRL": 5.65},
            "BRL": {"USD": 0.19, "EUR": 0.18},
        }

    def test_conversao_usd_to_brl(self):
        result = converter.converter(10, 'USD', 'BRL', self.taxas)
        self.assertEqual(result, Decimal('52.00'))

    def test_conversao_eur_to_usd(self):
        result = converter.converter(5, 'EUR', 'USD', self.taxas)
        expected = (Decimal('5') * Decimal(str(self.taxas['EUR']['USD']))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.assertEqual(result, expected)

    def test_conversao_zero(self):
        result = converter.converter(0, 'USD', 'EUR', self.taxas)
        self.assertEqual(result, Decimal('0.00'))

    def test_valor_negativo(self):
        stderr = io.StringIO()
        with self.assertRaises(SystemExit) as cm, redirect_stderr(stderr):
            converter.converter(-1, 'USD', 'BRL', self.taxas)
        self.assertEqual(cm.exception.code, 1)
        self.assertEqual(stderr.getvalue().strip(), "Erro: insira um valor numérico válido")

    def test_moeda_invalida_origem(self):
        stderr = io.StringIO()
        with self.assertRaises(SystemExit) as cm, redirect_stderr(stderr):
            converter.converter(10, 'ABC', 'USD', self.taxas)
        self.assertEqual(cm.exception.code, 1)
        self.assertEqual(stderr.getvalue().strip(), "Erro: moeda não suportada")

    def test_moeda_invalida_destino(self):
        stderr = io.StringIO()
        with self.assertRaises(SystemExit) as cm, redirect_stderr(stderr):
            converter.converter(10, 'USD', 'XYZ', self.taxas)
        self.assertEqual(cm.exception.code, 1)
        self.assertEqual(stderr.getvalue().strip(), "Erro: moeda não suportada")

    def test_formato_valor_invalido(self):
        stderr = io.StringIO()
        with self.assertRaises(SystemExit) as cm, redirect_stderr(stderr):
            converter.converter('abc', 'USD', 'BRL', self.taxas)
        self.assertEqual(cm.exception.code, 1)
        self.assertEqual(stderr.getvalue().strip(), "Erro: insira um valor numérico válido")

    def test_load_taxas_arquivo_inexistente(self):
        original = converter.JSON_FILE
        converter.JSON_FILE = 'nao_existe.json'
        stderr = io.StringIO()
        with self.assertRaises(SystemExit) as cm, redirect_stderr(stderr):
            converter.load_taxas()
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(stderr.getvalue().strip(), "Erro: não foi possível ler taxas de câmbio")
        converter.JSON_FILE = original

if __name__ == '__main__':
    unittest.main()
