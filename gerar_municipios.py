"""
Gera dados/municipios.json com os 5.571 municípios do Brasil a partir de APIs públicas:

  - IBGE Localidades  -> nome, UF, região geográfica imediata e intermediária
  - IBGE SIDRA        -> população residente (Censo 2022, tabela 4709)
  - Wikidata (SPARQL) -> bandeira (P41), brasão (P94) e mapa de localização (P242)

O jogo lê esse arquivo local (rápido e funciona mesmo se as APIs estiverem fora do ar).
Se o arquivo não existir, o jogo busca os dados direto da API do IBGE.

Uso:  python gerar_municipios.py
"""
import json
import os
import urllib.parse
import urllib.request
from datetime import date

USER_AGENT = "forca-brasil-gerador/1.0 (recurso educacional)"

URL_IBGE = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios?view=nivelado"
URL_SIDRA = "https://apisidra.ibge.gov.br/values/t/4709/n6/all/v/93/p/all"
URL_WIKIDATA = "https://query.wikidata.org/sparql"

CONSULTA_WIKIDATA = """
SELECT ?ibge (SAMPLE(?f) AS ?bandeira) (SAMPLE(?b) AS ?brasao) (SAMPLE(?m) AS ?mapa) WHERE {
  ?item wdt:P1585 ?ibge .
  FILTER(STRLEN(?ibge) = 7)
  OPTIONAL { ?item wdt:P41 ?f }
  OPTIONAL { ?item wdt:P94 ?b }
  OPTIONAL { ?item wdt:P242 ?m }
} GROUP BY ?ibge
"""

# Códigos IBGE das 27 capitais (26 capitais estaduais + Brasília)
CAPITAIS = {
    1200401, 2704302, 1600303, 1302603, 2927408, 2304400, 5300108, 3205309, 5208707,
    2111300, 5103403, 5002704, 3106200, 1501402, 2507507, 4106902, 2611606, 2211001,
    3304557, 2408102, 4314902, 1100205, 1400100, 4205407, 3550308, 2800308, 1721000,
}


def baixar_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def corrigir_texto(texto):
    """A API do IBGE traz '¿' no lugar do travessão em alguns nomes de região (ex.: 'Ilhéus ¿ Itabuna')."""
    return texto.replace("¿", "-")


def nome_arquivo_commons(uri):
    """'http://commons.wikimedia.org/wiki/Special:FilePath/Bandeira%20de%20X.svg' -> 'Bandeira de X.svg'"""
    if not uri:
        return ""
    return urllib.parse.unquote(uri.rsplit("/", 1)[-1])


def main():
    print("1/3 Baixando municípios do IBGE...")
    municipios_ibge = baixar_json(URL_IBGE)

    print("2/3 Baixando população (Censo 2022) do SIDRA/IBGE...")
    linhas_sidra = baixar_json(URL_SIDRA)[1:]  # a primeira linha é o cabeçalho
    populacao = {}
    for linha in linhas_sidra:
        if linha["V"].isdigit():
            populacao[int(linha["D1C"])] = int(linha["V"])

    print("3/3 Baixando bandeiras, brasões e mapas do Wikidata...")
    url_wd = URL_WIKIDATA + "?" + urllib.parse.urlencode({"query": CONSULTA_WIKIDATA, "format": "json"})
    imagens = {}
    for r in baixar_json(url_wd)["results"]["bindings"]:
        codigo = int(r["ibge"]["value"])
        imagens[codigo] = {
            "b": nome_arquivo_commons(r.get("bandeira", {}).get("value")),
            "br": nome_arquivo_commons(r.get("brasao", {}).get("value")),
            "m": nome_arquivo_commons(r.get("mapa", {}).get("value")),
        }

    municipios = []
    for m in municipios_ibge:
        codigo = m["municipio-id"]
        item = {
            "c": codigo,
            "n": corrigir_texto(m["municipio-nome"]),
            "uf": m["UF-sigla"],
            "ri": corrigir_texto(m["regiao-intermediaria-nome"]),
            "rm": corrigir_texto(m["regiao-imediata-nome"]),
        }
        if codigo in populacao:
            item["p"] = populacao[codigo]
        if codigo in CAPITAIS:
            item["cap"] = 1
        # Grava só as imagens que existem, para deixar o arquivo menor
        for chave, valor in imagens.get(codigo, {}).items():
            if valor:
                item[chave] = valor
        municipios.append(item)

    municipios.sort(key=lambda x: x["c"])

    saida = {
        "geradoEm": date.today().isoformat(),
        "fontes": {
            "municipios": URL_IBGE,
            "populacao": "IBGE SIDRA, tabela 4709 (Censo 2022)",
            "imagens": "Wikidata (P41 bandeira, P94 brasão, P242 mapa) / Wikimedia Commons",
        },
        "municipios": municipios,
    }

    os.makedirs("dados", exist_ok=True)
    destino = os.path.join("dados", "municipios.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, separators=(",", ":"))

    com_bandeira = sum(1 for m in municipios if "b" in m)
    com_imagem = sum(1 for m in municipios if "b" in m or "br" in m or "m" in m)
    print(f"Gerado: {destino}")
    print(f"  Municípios: {len(municipios)}")
    print(f"  Com população: {sum(1 for m in municipios if 'p' in m)}")
    print(f"  Com bandeira: {com_bandeira} | com alguma imagem: {com_imagem}")
    print(f"  Capitais: {sum(1 for m in municipios if 'cap' in m)}")


if __name__ == "__main__":
    main()
