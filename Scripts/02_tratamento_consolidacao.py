import re
from pathlib import Path
import pandas as pd
from html import unescape




PASTA_PROJETO = Path(__file__).resolve().parents[1]
PASTA_BRUTOS = PASTA_PROJETO / "Dados Brutos"
PASTA_TRATADOS = PASTA_PROJETO / "Dados Tratados"
PASTA_RELATORIOS = PASTA_PROJETO / "Relatorios"

PASTA_TRATADOS.mkdir(exist_ok=True)
PASTA_RELATORIOS.mkdir(exist_ok=True)

arquivos = sorted(PASTA_BRUTOS.glob("20*.csv"))

def limpar_texto_html(valor):
    if pd.isna(valor):
        return pd.NA

    texto = str(valor)

    # Decodifica entidades HTML repetidamente
    for _ in range(5):
        texto_anterior = texto
        texto = unescape(texto)

        if texto == texto_anterior:
            break

    # Remove tags HTML, preservando o conteúdo textual
    texto = re.sub(r"<[^>]+>", " ", texto)

    # Corrige espaços especiais e repetidos
    texto = texto.replace("\xa0", " ")
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto if texto else pd.NA

if len(arquivos) != 7:
    raise ValueError(
        f"Foram encontrados {len(arquivos)} arquivos. "
        "O esperado é encontrar 7 arquivos CSV."
    )

bases = []
linhas_por_arquivo = []

print("\nINICIANDO TRATAMENTO E CONSOLIDAÇÃO\n")

for arquivo in arquivos:
    print(f"Lendo e tratando {arquivo.name}...")

    df = pd.read_csv(
        arquivo,
        sep=";",
        encoding="utf-8",
        dtype="string",
        low_memory=False
    )

    linhas_originais = len(df)

    # Remove espaços no início e no fim e padroniza espaços repetidos

    colunas_textuais = [
        "nome_instituicao",
        "esfera",
        "municipio_instituicao",
        "uf",
        "descricao_catmat",
        "unidade_fornecimento",
        "generico",
        "modalidade_compra",
        "tipo_compra",
        "unidade_medida",
        "unidade_fornecimento_capacidade",
        "fornecedor",
        "fabricante"
    ]
    
    for coluna in colunas_textuais:
        df[coluna] = df[coluna].map(limpar_texto_html)
    
    # Padroniza espaços nas demais colunas
    for coluna in df.columns:
        df[coluna] = (
            df[coluna]
            .astype("string")
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
            .replace("", pd.NA)
        )

        # Conversão do ano
    df["ano_compra"] = pd.to_numeric(
        df["ano_compra"],
        errors="coerce"
    ).astype("Int64")

    # Conversão das datas
    for coluna in ["compra", "insercao"]:
        df[coluna] = pd.to_datetime(
            df[coluna],
            format="%d/%m/%Y",
            errors="coerce"
        )

    # Conversão dos campos numéricos
    for coluna in [
        "capacidade",
        "qtd_itens_comprados",
        "preco_unitario",
        "preco_total"
    ]:
        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        ).astype("Float64")

    linhas_por_arquivo.append(
        {
            "arquivo": arquivo.name,
            "linhas_brutas": linhas_originais
        }
    )

    bases.append(df)

print("\nConcatenando os sete anos...")

bps = pd.concat(
    bases,
    ignore_index=True
)

linhas_antes = len(bps)

# Remove somente registros totalmente idênticos
bps = bps.drop_duplicates().reset_index(drop=True)

linhas_depois = len(bps)
duplicados_removidos = linhas_antes - linhas_depois

# Validação: preço total versus quantidade x preço unitário
valor_calculado = (
    bps["qtd_itens_comprados"] * bps["preco_unitario"]
)

diferenca_valor = (
    bps["preco_total"] - valor_calculado
).abs()

divergencias_financeiras = int(
    (diferenca_valor > 0.01).fillna(False).sum()
)

arquivo_saida = (
    PASTA_TRATADOS /
    "BPS_20_26_Bruno_Briani.csv"
)

print("\nSalvando a base consolidada...")

bps.to_csv(
    arquivo_saida,
    sep=";",
    index=False,
    encoding="utf-8-sig",
    date_format="%d/%m/%Y",
    na_rep=""
)

resumo_arquivos = pd.DataFrame(linhas_por_arquivo)

relatorio = PASTA_RELATORIOS / "relatorio_consolidacao.txt"

with open(relatorio, "w", encoding="utf-8") as arquivo:
    arquivo.write("RELATÓRIO DE CONSOLIDAÇÃO — BPS 2020 A 2026\n\n")
    arquivo.write(resumo_arquivos.to_string(index=False))
    arquivo.write("\n\n")
    arquivo.write(f"Registros antes da limpeza: {linhas_antes}\n")
    arquivo.write(f"Duplicados removidos: {duplicados_removidos}\n")
    arquivo.write(f"Registros após a limpeza: {linhas_depois}\n")
    arquivo.write(
        "Divergências entre preço_total e "
        f"quantidade x preço_unitário: {divergencias_financeiras}\n"
    )

print("\nCONSOLIDAÇÃO CONCLUÍDA")
print(f"Registros antes da limpeza: {linhas_antes:,}")
print(f"Duplicados removidos: {duplicados_removidos:,}")
print(f"Registros finais: {linhas_depois:,}")
print(f"Divergências financeiras: {divergencias_financeiras:,}")
print(f"\nBase consolidada: {arquivo_saida}")
print(f"Relatório: {relatorio}")