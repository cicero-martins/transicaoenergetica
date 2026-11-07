"""Atualiza dados/sr_brasil_mundo.csv a partir do Our World in Data.

O Our World in Data redistribui a Statistical Review of World Energy
(Energy Institute). As participações usam o método de substituição.

Uso:
    python scripts/atualizar_sr.py            # baixa o CSV do OWID
    python scripts/atualizar_sr.py arquivo.csv  # usa um CSV já baixado
"""
import csv
import io
import sys
import urllib.request
from pathlib import Path

URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
SAIDA = Path(__file__).resolve().parent.parent / "dados" / "sr_brasil_mundo.csv"

REGIOES = {"Brazil": "Brasil", "World": "Mundo"}
COLUNAS = {
    "oil_share_energy": "petroleo",
    "gas_share_energy": "gas",
    "coal_share_energy": "carvao",
    "nuclear_share_energy": "nuclear",
    "hydro_share_energy": "hidraulica",
    "wind_share_energy": "eolica",
    "solar_share_energy": "solar",
    "biofuel_share_energy": "biocombustivel",
    "other_renewables_share_energy": "outras_ren",
}


def ler_fonte():
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).read_text(encoding="utf-8")
    with urllib.request.urlopen(URL, timeout=120) as resp:
        return resp.read().decode("utf-8")


def main():
    leitor = csv.DictReader(io.StringIO(ler_fonte()))
    linhas = []
    for r in leitor:
        if r["country"] not in REGIOES:
            continue
        valores = [r[c] for c in COLUNAS]
        if any(v == "" for v in valores):
            continue
        ano = int(r["year"])
        if ano < 1970:
            continue
        linhas.append([ano, REGIOES[r["country"]]] + [f"{float(v):.2f}" for v in valores])
    if not linhas:
        sys.exit("Nenhuma linha encontrada: o formato do arquivo do OWID pode ter mudado.")
    linhas.sort(key=lambda x: (x[1], x[0]))
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with SAIDA.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ano", "regiao"] + list(COLUNAS.values()))
        w.writerows(linhas)
    ultimo = max(l[0] for l in linhas)
    print(f"{SAIDA.name}: {len(linhas)} linhas, último ano {ultimo}")


if __name__ == "__main__":
    main()
