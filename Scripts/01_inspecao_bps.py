from pathlib import Path
import pandas as pd


# Localiza automaticamente as pastas do projeto
PASTA_PROJETO = Path(__file__).resolve().parents[1]
PASTA_DADOS = PASTA_PROJETO / "Dados Brutos"
PASTA_RELATORIOS = PASTA_PROJETO / "Relatorios"

PASTA_RELATORIOS.mkdir(exist_ok=True)

arquivos = sorted(PASTA_DADOS.glob("20*.csv"))

if len(arquivos) != 7:
    raise ValueError(
        f"Foram encontrados {len(arquivos)} arquivos CSV. "
        "O esperado é encontrar 7 arquivos, de 2020 a 2026."
    )

colunas_referencia = None
resultados = []

print("\nINICIANDO A INSPEÇÃO DOS ARQUIVOS BPS\n")

for arquivo in arquivos:
    ano_arquivo = arquivo.stem

    print(f"Lendo {arquivo.name}...")

    df = pd.read_csv(
        arquivo,
        sep=";",
        encoding="utf-8",
        dtype=str,
        low_memory=False
    )

    # Verifica se as colunas são iguais em todos os anos
    if colunas_referencia is None:
        colunas_referencia = list(df.columns)

    estrutura_igual = list(df.columns) == colunas_referencia

    # Verifica duplicidades completas
    duplicados = int(df.duplicated().sum())

    # Verifica divergências entre o ano do arquivo e ano_compra
    ano_informado = df["ano_compra"].astype("string").str.strip()

    anos_divergentes = int(
        (
            ano_informado.notna()
            & ano_informado.ne("")
            & ano_informado.ne(ano_arquivo)
        ).sum()
    )

    # Validação das datas
    datas_invalidas = {}

    for coluna in ["compra", "insercao"]:
        valores = df[coluna].astype("string").str.strip()
        preenchidos = valores.notna() & valores.ne("")

        datas_convertidas = pd.to_datetime(
            valores.where(preenchidos),
            format="%d/%m/%Y",
            errors="coerce"
        )

        datas_invalidas[coluna] = int(
            (preenchidos & datas_convertidas.isna()).sum()
        )

    # Validação dos campos numéricos
    numericos_invalidos = {}

    for coluna in [
        "capacidade",
        "qtd_itens_comprados",
        "preco_unitario",
        "preco_total"
    ]:
        valores = df[coluna].astype("string").str.strip()
        preenchidos = valores.notna() & valores.ne("")

        valores_convertidos = pd.to_numeric(
            valores.where(preenchidos),
            errors="coerce"
        )

        numericos_invalidos[coluna] = int(
            (preenchidos & valores_convertidos.isna()).sum()
        )

    resultados.append(
        {
            "arquivo": arquivo.name,
            "ano": ano_arquivo,
            "linhas": len(df),
            "colunas": len(df.columns),
            "estrutura_igual": estrutura_igual,
            "duplicados_completos": duplicados,
            "anos_divergentes": anos_divergentes,
            "compra_data_invalida": datas_invalidas["compra"],
            "insercao_data_invalida": datas_invalidas["insercao"],
            "capacidade_invalida": numericos_invalidos["capacidade"],
            "quantidade_invalida": numericos_invalidos["qtd_itens_comprados"],
            "preco_unitario_invalido": numericos_invalidos["preco_unitario"],
            "preco_total_invalido": numericos_invalidos["preco_total"]
        }
    )

    exemplo = df["descricao_catmat"].dropna()

    if not exemplo.empty:
        print(f"  Exemplo de produto: {exemplo.iloc[0]}")

    print(f"  Linhas: {len(df):,}")
    print(f"  Duplicados: {duplicados:,}")
    print(f"  Estrutura igual: {estrutura_igual}\n")

resumo = pd.DataFrame(resultados)

arquivo_saida = PASTA_RELATORIOS / "resumo_inspecao.csv"

resumo.to_csv(
    arquivo_saida,
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("\nRESUMO FINAL\n")
print(resumo.to_string(index=False))
print(f"\nRelatório salvo em: {arquivo_saida}")