#!/usr/bin/env python3
"""
Conversor de Moedas CLI

Este script permite converter valores entre USD, EUR e BRL usando taxas definidas em taxas.json.
"""
import json
import os
import sys
from decimal import Decimal, ROUND_HALF_UP
import argparse

# Caminho do arquivo de taxas
JSON_FILE = os.path.join(os.path.dirname(__file__), 'taxas.json')


def load_taxas():
    """
    Carrega as taxas de câmbio do arquivo JSON.
    Em caso de falha, exibe mensagem de erro e encerra com código 2.
    """
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        print("Erro: não foi possível ler taxas de câmbio", file=sys.stderr)
        sys.exit(2)


def converter(valor, origem, destino, taxas):
    """
    Converte um valor de origem para destino usando as taxas fornecidas.
    Valida moedas e valor, gerando mensagens de erro adequadas.
    """
    origem = origem.upper()
    destino = destino.upper()

    # Validação de moeda
    if origem not in taxas or destino not in taxas[origem]:
        print("Erro: moeda não suportada", file=sys.stderr)
        sys.exit(1)

    # Validação de valor numérico
    try:
        dec_valor = Decimal(str(valor))
    except Exception:
        print("Erro: insira um valor numérico válido", file=sys.stderr)
        sys.exit(1)

    if dec_valor < 0:
        print("Erro: insira um valor numérico válido", file=sys.stderr)
        sys.exit(1)

    # Cálculo e arredondamento
    taxa = Decimal(str(taxas[origem][destino]))
    resultado = (dec_valor * taxa).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return resultado


def main():
    parser = argparse.ArgumentParser(description='Conversor de Moedas CLI')
    parser.add_argument('-f', '--from', dest='origem', required=True,
                        help='Moeda de origem: USD, EUR ou BRL')
    parser.add_argument('-t', '--to', dest='destino', required=True,
                        help='Moeda de destino: USD, EUR ou BRL')
    parser.add_argument('-a', '--amount', dest='amount', required=True,
                        help='Valor a ser convertido (>= 0, até 2 casas decimais)')
    args = parser.parse_args()

    taxas = load_taxas()
    resultado = converter(args.amount, args.origem, args.destino, taxas)

    # Exibe o resultado formatado com duas casas decimais
    print(f"{resultado:.2f}")
    sys.exit(0)


if __name__ == '__main__':
    main()
