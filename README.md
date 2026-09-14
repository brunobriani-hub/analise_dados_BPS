# Dashboard de Compras PÃºblicas em SaÃºde â€” BPS 2020â€“2026

## Sobre o projeto

Este projeto apresenta um dashboard analÃ­tico desenvolvido no Power BI a partir dos dados pÃºblicos do Banco de PreÃ§os em SaÃºde (BPS), do MinistÃ©rio da SaÃºde, abrangendo os anos de 2020 a 2026.

O objetivo Ã© transformar os registros de compras de medicamentos, materiais hospitalares e dispositivos mÃ©dicos em indicadores e visualizaÃ§Ãµes que apoiem a exploraÃ§Ã£o dos gastos, das quantidades adquiridas, dos compradores, dos fornecedores e das variaÃ§Ãµes de preÃ§o.

> **ObservaÃ§Ã£o:** diferenÃ§as de preÃ§os nÃ£o representam automaticamente economia, sobrepreÃ§o ou irregularidade. Fabricante, apresentaÃ§Ã£o, unidade de fornecimento, quantidade, localidade, modalidade de compra, perÃ­odo e condiÃ§Ãµes de negociaÃ§Ã£o podem afetar os valores.

## Objetivos

- Consolidar os arquivos anuais do BPS em uma Ãºnica base histÃ³rica.
- Avaliar a evoluÃ§Ã£o dos valores registrados entre 2020 e 2026.
- Identificar estados, instituiÃ§Ãµes, produtos e fornecedores com maior participaÃ§Ã£o.
- Comparar mÃ©dia, mediana, mÃ­nimo e mÃ¡ximo dos preÃ§os unitÃ¡rios.
- Permitir anÃ¡lises interativas por produto, unidade, ano e UF.
- Evidenciar oportunidades para investigaÃ§Ãµes mais detalhadas sobre diferenÃ§as de preÃ§os.

## Fonte dos dados

- **Fonte:** Banco de PreÃ§os em SaÃºde â€” BPS, MinistÃ©rio da SaÃºde.
- **Portal:** [Portal de Dados Abertos do MinistÃ©rio da SaÃºde](https://dadosabertos.saude.gov.br/dataset/bps)
- **PerÃ­odo:** 2020 a 2026.
- **Formato original:** sete arquivos CSV anuais.
- **Data de acesso:** setembro de 2026.

## PreparaÃ§Ã£o e consolidaÃ§Ã£o

A preparaÃ§Ã£o foi realizada em Python com a biblioteca pandas. O script percorre os sete arquivos CSV da pasta `Dados Brutos`, aplica os tratamentos e concatena os registros em uma base histÃ³rica.

### Tratamentos realizados

- validaÃ§Ã£o da presenÃ§a dos sete arquivos anuais;
- conferÃªncia da estrutura de 25 colunas;
- leitura com delimitador `;` e codificaÃ§Ã£o UTF-8;
- padronizaÃ§Ã£o de espaÃ§os em campos textuais;
- correÃ§Ã£o de caracteres e entidades HTML nas descriÃ§Ãµes CATMAT;
- remoÃ§Ã£o de tags HTML preservando seu conteÃºdo textual;
- conversÃ£o das datas de compra e inserÃ§Ã£o;
- conversÃ£o dos campos de quantidade e preÃ§o para tipos numÃ©ricos;
- preservaÃ§Ã£o de CNPJs e cÃ³digos identificadores como texto;
- verificaÃ§Ã£o da correspondÃªncia entre o ano do arquivo e `ano_compra`;
- identificaÃ§Ã£o e remoÃ§Ã£o apenas de registros completamente duplicados;
- validaÃ§Ã£o de `preco_total` em relaÃ§Ã£o a quantidade Ã— preÃ§o unitÃ¡rio.

### Resultado da consolidaÃ§Ã£o

| Indicador | Resultado |
|---|---:|
| Registros antes da limpeza | 342.716 |
| Registros duplicados removidos | 19 |
| Registros finais | 342.697 |
| Colunas | 25 |
| DivergÃªncias financeiras identificadas | 0 |
| Registros com HTML remanescente em `descricao_catmat` | 0 |

DistribuiÃ§Ã£o dos registros finais:

| Ano | Registros |
|---:|---:|
| 2020 | 84.819 |
| 2021 | 83.622 |
| 2022 | 88.991 |
| 2023 | 31.992 |
| 2024 | 26.242 |
| 2025 | 26.214 |
| 2026 | 817 |

O processamento gera localmente o arquivo `BPS_20_26_Bruno_Briani.csv`. Para disponibilizaÃ§Ã£o no GitHub, a base consolidada foi compactada como `BPS_20_26_Bruno_Briani.zip`, reduzindo o tamanho de aproximadamente 129,42 MB para 18,42 MB.

## Principais colunas

| Coluna | DescriÃ§Ã£o e uso |
|---|---|
| `ano_compra` | Ano de realizaÃ§Ã£o da compra |
| `compra` | Data da compra |
| `nome_instituicao` | InstituiÃ§Ã£o compradora |
| `esfera` | Esfera administrativa da instituiÃ§Ã£o |
| `municipio_instituicao` | MunicÃ­pio da instituiÃ§Ã£o |
| `uf` | Unidade da FederaÃ§Ã£o da instituiÃ§Ã£o |
| `codigo_br` | CÃ³digo de identificaÃ§Ã£o do item no CATMAT |
| `descricao_catmat` | DescriÃ§Ã£o do medicamento ou material |
| `unidade_fornecimento` | Unidade utilizada no fornecimento |
| `modalidade_compra` | Modalidade utilizada na aquisiÃ§Ã£o |
| `fornecedor` | Nome do fornecedor |
| `fabricante` | Nome do fabricante |
| `qtd_itens_comprados` | Quantidade adquirida |
| `preco_unitario` | PreÃ§o unitÃ¡rio registrado |
| `preco_total` | Valor total registrado |

## Modelagem no Power BI

Foi utilizada uma tabela fato, `Fato_BPS`, relacionada a uma dimensÃ£o calendÃ¡rio. O relacionamento ativo entre a data de compra e a dimensÃ£o permite anÃ¡lises anuais e temporais. As medidas foram organizadas em uma tabela exclusiva denominada `Medidas`.

## KPIs

| KPI | DefiniÃ§Ã£o |
|---|---|
| Valor Total Registrado | Soma de `preco_total` no contexto dos filtros |
| Quantidade Total de Itens | Soma de `qtd_itens_comprados` |
| NÃºmero de Registros | Quantidade de registros apÃ³s os filtros |
| InstituiÃ§Ãµes Compradoras | Contagem distinta das instituiÃ§Ãµes |
| Fornecedores | Contagem distinta dos fornecedores |
| PreÃ§o UnitÃ¡rio MÃ©dio Ponderado | Valor total dividido pela quantidade total |
| PreÃ§o UnitÃ¡rio MÃ©dio | MÃ©dia aritmÃ©tica dos preÃ§os unitÃ¡rios |
| PreÃ§o UnitÃ¡rio Mediano | Mediana dos preÃ§os unitÃ¡rios |
| PreÃ§o UnitÃ¡rio MÃ­nimo e MÃ¡ximo | Extremos observados no contexto selecionado |
| Amplitude do PreÃ§o UnitÃ¡rio | DiferenÃ§a entre preÃ§o mÃ¡ximo e mÃ­nimo |

## PÃ¡ginas do dashboard

### 1. VisÃ£o Geral

Apresenta os principais KPIs, a evoluÃ§Ã£o anual do valor registrado, as UFs de maior participaÃ§Ã£o e a distribuiÃ§Ã£o por esfera administrativa.

![VisÃ£o Geral](Imagens/visao-geral.png)

### 2. Produtos e Fornecedores

Permite explorar os produtos mais relevantes, fornecedores, fabricantes e a participaÃ§Ã£o financeira nos registros.

![Produtos e Fornecedores](Imagens/produtos-fornecedores.png)

### 3. AnÃ¡lise de PreÃ§os

Compara mÃ©dia, mediana, mÃ­nimo, mÃ¡ximo e amplitude dos preÃ§os. Inclui evoluÃ§Ã£o anual, comparaÃ§Ã£o entre UFs e fornecedores e filtros por produto, unidade, ano e UF.

![AnÃ¡lise de PreÃ§os](Imagens/analise-precos.png)

### 4. Detalhamento das Compras

Aprofunda a anÃ¡lise territorial e institucional das aquisiÃ§Ãµes. A pÃ¡gina apresenta a distribuiÃ§Ã£o geogrÃ¡fica dos municÃ­pios com maior valor registrado, o ranking das instituiÃ§Ãµes compradoras, a participaÃ§Ã£o dos principais fabricantes e as modalidades de compra mais utilizadas. Os visuais podem ser filtrados por ano, UF, esfera administrativa e modalidade de compra.

![Detalhamento das Compras](Imagens/detalhamento-compras.png)

## Principais anÃ¡lises e descobertas

- A base consolidada possui 342.697 registros vÃ¡lidos entre 2020 e 2026.
- Os anos de 2020, 2021 e 2022 concentram o maior nÃºmero de registros; hÃ¡ reduÃ§Ã£o relevante a partir de 2023.
- A diferenÃ§a entre mÃ©dia e mediana dos preÃ§os unitÃ¡rios demonstra uma distribuiÃ§Ã£o assimÃ©trica, influenciada por itens de naturezas e valores muito diferentes.
- A comparaÃ§Ã£o geral de preÃ§os deve ser interpretada com cautela, pois a base reÃºne produtos, apresentaÃ§Ãµes e unidades distintas.
- Os filtros de produto e unidade de fornecimento sÃ£o essenciais para comparaÃ§Ãµes coerentes entre preÃ§os.
- Valores extremos devem ser tratados como oportunidades de investigaÃ§Ã£o, e nÃ£o como evidÃªncia automÃ¡tica de irregularidade.
- A anÃ¡lise detalhada permite identificar concentraÃ§Ãµes territoriais e institucionais dos valores registrados, alÃ©m da participaÃ§Ã£o dos fabricantes e das modalidades de compra.
- O mapa municipal deve ser interpretado em conjunto com o valor total e o nÃºmero de registros exibidos nas dicas de ferramentas.

## RecomendaÃ§Ãµes

- Comparar preÃ§os somente entre itens equivalentes, considerando cÃ³digo CATMAT, apresentaÃ§Ã£o, capacidade e unidade de fornecimento.
- Utilizar a mediana em conjunto com a mÃ©dia ponderada para reduzir a influÃªncia de valores extremos.
- Investigar registros muito afastados da distribuiÃ§Ã£o antes de formular conclusÃµes.
- Considerar quantidade, modalidade de compra, fornecedor, fabricante, localidade e perÃ­odo na interpretaÃ§Ã£o das diferenÃ§as.
- Manter a base atualizada e analisar 2026 separadamente, pois o ano possui cobertura parcial.

## LimitaÃ§Ãµes

- O BPS representa registros inseridos pelas instituiÃ§Ãµes e pode apresentar diferenÃ§as de cobertura entre anos e localidades.
- O ano de 2026 estÃ¡ incompleto e nÃ£o deve ser comparado diretamente com anos completos em totais anuais.
- Produtos com descriÃ§Ãµes semelhantes podem possuir apresentaÃ§Ãµes, capacidades ou unidades diferentes.
- O preÃ§o unitÃ¡rio mÃ©dio ponderado agregado perde significado quando produtos heterogÃªneos sÃ£o analisados simultaneamente.
- O dashboard evidencia padrÃµes e diferenÃ§as, mas nÃ£o comprova sobrepreÃ§o, economia ou irregularidade.

## Como reproduzir

1. Instalar Python 3 e criar um ambiente virtual.
2. Instalar as dependÃªncias do projeto, incluindo pandas.
3. Baixar os arquivos do BPS de 2020 a 2026.
4. Colocar os arquivos na pasta `Dados Brutos` com os nomes `2020.csv` a `2026.csv`.
5. Executar o script de validaÃ§Ã£o, quando disponÃ­vel.
6. Executar:

```powershell
.\.venv\Scripts\python.exe .\Scripts\02_tratamento_consolidacao.py
```

7. Confirmar a geraÃ§Ã£o de `Dados Tratados/BPS_20_26_Bruno_Briani.csv`.
8. Para publicaÃ§Ã£o no GitHub, compactar o CSV como `Dados Tratados/BPS_20_26_Bruno_Briani.zip`.
8. Abrir o arquivo do Power BI e atualizar a fonte de dados, se necessÃ¡rio.

## Estrutura sugerida do repositÃ³rio

```text
ProjetoSUS/
â”œâ”€â”€ Dashboard/
â”‚   â””â”€â”€ Dashboard_BPS_2020_2026.pbix
â”œâ”€â”€ Dados Tratados/
â”‚   â””â”€â”€ BPS_20_26_Bruno_Briani.zip
â”œâ”€â”€ Imagens/
â”‚   â”œâ”€â”€ visao-geral.png
â”‚   â”œâ”€â”€ produtos-fornecedores.png
â”‚   â”œâ”€â”€ analise-precos.png
â”‚   â””â”€â”€ detalhamento-compras.png
â”œâ”€â”€ Relatorios/
â”‚   â””â”€â”€ relatorio_consolidacao.txt
â”œâ”€â”€ Scripts/
â”‚   â””â”€â”€ 02_tratamento_consolidacao.py
â”œâ”€â”€ README.md
â””â”€â”€ requirements.txt
```

Os arquivos brutos podem ser omitidos do GitHub devido ao tamanho, desde que sejam fornecidas instruÃ§Ãµes e a fonte oficial para reproduÃ§Ã£o.

## Dashboard e vÃ­deo

- **Dashboard interativo:** [Acessar no Power BI](https://app.powerbi.com/view?r=eyJrIjoiNmE5OTBjN2EtYWJjMy00ZDdiLTg1N2EtZWI2ZDkyZDdiOGE1IiwidCI6IjJjZjdkNGQ1LWJkMWItNDk1Ni1hY2Y4LTI5OTUzOTliMjE2OCJ9)
- **Dashboard/arquivo PBIX:** disponÃ­vel na pasta `Dashboard`.
- **VÃ­deo de apresentaÃ§Ã£o:** [inserir link pÃºblico ou acessÃ­vel](COLE_AQUI_O_LINK_DO_VIDEO)
- **RepositÃ³rio:** [inserir link do GitHub](https://github.com/brunobriani-hub/analise_dados_BPS)

## Tecnologias

- Python
- pandas
- Power BI
- Power Query
- DAX
- Git e GitHub

## Autor

**Bruno Briani de Paula**

- GitHub: [brunobriani-hub](https://github.com/brunobriani-hub)

