"""
Projeto de Portfólio 1: Scraper de Preços
-------------------------------------------
Esse script coleta o preço de um produto em um site e salva
os dados em um arquivo CSV (planilha) com data e hora da coleta.

Ideia: rodar esse script todo dia pra acompanhar a variação
de preço de um produto ao longo do tempo — muito usado por
lojas, e-commerces e consumidores que monitoram promoções.

Bibliotecas usadas:
- requests: pra baixar o HTML da página
- BeautifulSoup: pra "ler" o HTML e encontrar o preço
- csv: pra salvar os dados numa planilha
- datetime: pra registrar quando a coleta foi feita
"""

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

# ---------------------------------------------------------
# CONFIGURAÇÃO: troque essa URL pelo produto que quiser
# monitorar. Esse exemplo usa um site fictício de testes
# (books.toscrape.com), feito especialmente pra praticar
# web scraping sem violar termos de uso de sites reais.
# ---------------------------------------------------------
URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
ARQUIVO_SAIDA = "precos_coletados.csv"


def coletar_preco(url):
    """
    Faz a requisição no site e extrai o preço do produto.
    Retorna um dicionário com nome, preço e data da coleta.
    """
    # Simula um navegador real, pra evitar bloqueios simples
    headers = {"User-Agent": "Mozilla/5.0"}

    resposta = requests.get(url, headers=headers)
    resposta.raise_for_status()  # gera erro se a página não carregar

    soup = BeautifulSoup(resposta.text, "html.parser")

    # Esses seletores mudam de site pra site — aqui são
    # específicos do books.toscrape.com (site de prática)
    nome_produto = soup.find("h1").text.strip()
    preco_texto = soup.find("p", class_="price_color").text.strip()

    return {
        "produto": nome_produto,
        "preco": preco_texto,
        "coletado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def salvar_no_csv(dados, arquivo):
    """
    Salva os dados coletados no arquivo CSV.
    Se o arquivo ainda não existe, cria com o cabeçalho.
    Se já existe, apenas adiciona uma nova linha (append).
    """
    arquivo_existe = os.path.isfile(arquivo)

    with open(arquivo, mode="a", newline="", encoding="utf-8") as f:
        campos = ["produto", "preco", "coletado_em"]
        writer = csv.DictWriter(f, fieldnames=campos)

        if not arquivo_existe:
            writer.writeheader()  # escreve o cabeçalho só na primeira vez

        writer.writerow(dados)


if __name__ == "__main__":
    print("Coletando preço...")
    dados = coletar_preco(URL)
    print(f"Produto: {dados['produto']}")
    print(f"Preço: {dados['preco']}")
    print(f"Coletado em: {dados['coletado_em']}")

    salvar_no_csv(dados, ARQUIVO_SAIDA)
    print(f"\nDados salvos em '{ARQUIVO_SAIDA}'")