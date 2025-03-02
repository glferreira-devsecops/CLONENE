from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Inicializar a sessão Spark
spark = SparkSession.builder \
    .appName("Processamento População") \
    .getOrCreate()

# a. Carregar o arquivo CSV
df = spark.read.csv(
    "populacao_paises.csv",
    header=True,
    inferSchema=True
)

# b. Filtrar países com população >= 1 milhão
df_filtrado = df.filter(F.col("População 2024") >= 1000000)

# c. Calcular população projetada para 2030
df_2030 = df_filtrado.withColumn(
    "População em 2030",
    F.round(
        F.col("População 2024") * F.pow(1 + (F.col("Variação Populacional (%)") / 100), 6),
        0
    ).cast("integer")
)

# d. Salvar resultado em Parquet
df_2030.write \
    .mode("overwrite") \
    .parquet("populacao_paises_processado.parquet")

# Encerrar sessão Spark
spark.stop()