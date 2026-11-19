# forca-brasil

Jogo da forca educacional com dois modos:

- **Estados do Brasil**: as 27 UF, divididas em níveis por região.
- **Municípios do Brasil**: os 5.571 municípios, filtráveis por UF (ou Brasil todo), com dificuldade e número de rodadas.

## Dados dos municípios

O modo municípios usa o arquivo `dados/municipios.json`, gerado a partir de APIs públicas:

| Dado | Fonte |
|---|---|
| Nome, UF, regiões geográficas imediata e intermediária | [API de Localidades do IBGE](https://servicodados.ibge.gov.br/api/docs/localidades) |
| População (Censo 2022) | [SIDRA/IBGE, tabela 4709](https://apisidra.ibge.gov.br/) |
| Bandeira, brasão e mapa de localização | [Wikidata](https://www.wikidata.org/) / Wikimedia Commons |

Para atualizar os dados (por exemplo, após um novo censo):

```
python gerar_municipios.py
```

Se o arquivo local não carregar, o jogo busca os municípios direto da API do IBGE e as imagens no Wikidata
(nesse caso, sem população, a dificuldade não é aplicada).

### Como o jogo usa esses dados

- **Dicas** são geradas automaticamente (estado, região, capital, população, região geográfica);
  frases que entregariam o nome do município são descartadas.
- **Imagem**: bandeira do município → brasão → mapa de localização → bandeira do estado.
- **Dificuldade** pelo ranking de população: Fácil = 10% mais populosos + capitais; Médio = até 40%; Difícil = o restante.
- **Hífen e apóstrofo** (ex.: Ji-Paraná, Espigão D'Oeste) já aparecem revelados.
- O professor sorteia os municípios e os códigos ficam salvos na sala, para todos os alunos jogarem a mesma sequência.
