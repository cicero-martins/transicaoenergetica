# Matriz energética brasileira

Página de apoio da disciplina **Transição Energética e Sociedade** (PUC-PR Digital):
evolução da matriz energética brasileira desde 1970 com dados do Balanço Energético
Nacional (EPE) e comparação internacional pela *Statistical Review of World Energy*.

A página é publicada automaticamente pelo GitHub Pages. Qualquer pessoa abre pelo
link, sem login.

## Estrutura

```
dados/
  ben_oie.csv            BEN: participação (%) de cada fonte na oferta interna, e total em Mtep
  sr_brasil_mundo.csv    Statistical Review (via Our World in Data): Brasil e Mundo
modelo/
  index.html             modelo da página (texto, estilo e gráficos)
  vendor/d3.min.js       biblioteca de gráficos D3 (licença ISC)
scripts/
  atualizar_sr.py        baixa os dados mais recentes da Statistical Review
  gerar_pagina.py        monta site/index.html com os dados embutidos
.github/workflows/
  publicar.yml           gera e publica a página a cada alteração e uma vez por mês
```

## Publicar pela primeira vez (uma vez só, ~10 minutos)

1. Entre no [GitHub](https://github.com) (crie uma conta gratuita, se não tiver).
2. Crie um repositório **público** (este se chama `transicaoenergetica`)
   (botão **New repository**). Não marque nenhuma opção de README.
3. Na página do repositório vazio, clique em **uploading an existing file** e arraste
   **todo o conteúdo desta pasta** (as pastas `dados`, `modelo`, `scripts`, `.github`
   e os arquivos soltos). Clique em **Commit changes**.
   - A pasta `.github` começa com ponto e pode estar oculta no seu computador.
     No Windows, ative "Itens ocultos" no Explorador; no macOS, `Cmd + Shift + .` no Finder.
     Se preferir, crie o arquivo pelo site: **Add file → Create new file**, nome
     `.github/workflows/publicar.yml`, e cole o conteúdo do arquivo.
4. Vá em **Settings → Pages** e, em **Build and deployment → Source**, escolha
   **GitHub Actions**.
5. Vá na aba **Actions**, abra **Publicar página** e clique em **Run workflow**.
   Em 1–2 minutos o link aparece no resumo da execução:
   `https://cicero-martins.github.io/transicaoenergetica/`

Esse é o link para compartilhar com os alunos.

## O que acontece automaticamente

- Qualquer alteração enviada ao repositório (pelo site do GitHub, inclusive) gera e
  publica a página de novo.
- Todo dia 5, o GitHub busca os dados mais recentes da Statistical Review no Our World
  in Data, guarda no repositório e republica a página.
- Se o download falhar, a página é publicada com os dados que já estão no repositório.

## Atualização anual do BEN (manual, uma vez por ano)

A EPE publica o BEN do ano anterior em meados de cada ano. O site da EPE não tem um
endereço fixo para download automático, então essa atualização é feita à mão:

1. Em [BEN – Séries Históricas e Matrizes](https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/BEN-Series-Historicas-Completas),
   baixe a planilha do **Capítulo 1** e localize a **Tabela 1.3.a** (Evolução da oferta
   interna de energia, em mil tep).
2. Em `dados/ben_oie.csv`, acrescente uma linha para o novo ano. As colunas são
   participações (%) calculadas como valor da fonte ÷ TOTAL × 100, com uma casa decimal;
   `total_mtep` é o TOTAL ÷ 1000. A EPE às vezes revisa anos anteriores: confira também
   os últimos anos.
3. Atualize o nome da edição do BEN em `modelo/index.html` (seção "Fontes" e "Como citar").
4. Envie as alterações (pelo site: abra o arquivo, ícone de lápis, edite e **Commit**).
   A página é republicada sozinha.

Os textos e números da página são calculados a partir dos dados: ao acrescentar um ano,
"última década", destaques e comparações se ajustam sozinhos.

## Testar no computador (opcional)

```
python scripts/atualizar_sr.py
python scripts/gerar_pagina.py
```

e abra `site/index.html` no navegador. A página é um arquivo único: também pode ser
enviada direto ao ambiente virtual do curso, se preferir.

## Fontes

- EPE – Empresa de Pesquisa Energética. *Balanço Energético Nacional 2026: ano base 2025*.
  Séries Históricas Completas, Capítulo 1, Tabela 1.3.a.
- Energy Institute. *Statistical Review of World Energy*, via Our World in Data
  ([owid/energy-data](https://github.com/owid/energy-data), licença CC BY 4.0).
