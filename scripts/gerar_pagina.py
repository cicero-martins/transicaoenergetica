"""Gera o site estático em site/ a partir do modelo e dos CSVs em dados/.

Os dados são embutidos na página (funciona até aberta direto do disco)
e os CSVs são copiados para site/dados/ para download.

Uso:
    python scripts/gerar_pagina.py
"""
import csv
import datetime
import json
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"
MODELO = RAIZ / "modelo"
SITE = RAIZ / "site"

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]


def ler(nome):
    with (DADOS / nome).open(encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    out = []
    for r in linhas:
        out.append({k: (v if k == "regiao" else float(v)) for k, v in r.items()})
    return out


def main():
    ben = ler("ben_oie.csv")
    sr = ler("sr_paises.csv")
    for r in ben:
        r["ano"] = int(r["ano"])
    for r in sr:
        r["ano"] = int(r["ano"])
    hoje = datetime.date.today()
    dados = {
        "ben": ben,
        "sr": sr,
        "gerado": f"{MESES[hoje.month - 1]} de {hoje.year}",
    }
    html = (MODELO / "index.html").read_text(encoding="utf-8")
    marcador = "/*__DADOS__*/null"
    if marcador not in html:
        raise SystemExit("Marcador de dados não encontrado no modelo.")
    html = html.replace(marcador, json.dumps(dados, ensure_ascii=False, separators=(",", ":")))

    # D3 embutido: a página funciona como arquivo único (servidor, AVA, e-mail ou disco).
    tag_d3 = '<script src="vendor/d3.min.js"></script>'
    d3_js = (MODELO / "vendor" / "d3.min.js").read_text(encoding="utf-8")
    html = html.replace(tag_d3, "<script>\n" + d3_js.replace("</script", "<\\/script") + "\n</script>")

    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "dados").mkdir(parents=True)
    (SITE / "index.html").write_text(html, encoding="utf-8")
    for csv_file in DADOS.glob("*.csv"):
        shutil.copy(csv_file, SITE / "dados" / csv_file.name)
    (SITE / ".nojekyll").write_text("")
    print(f"site/index.html gerado ({len(ben)} anos do BEN, {len(sr)} linhas da Statistical Review)")


if __name__ == "__main__":
    main()
