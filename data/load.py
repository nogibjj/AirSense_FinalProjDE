from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def clean_column_names(df):
    """
    Cleans column names by replacing invalid characters with underscores.
    """
    for col_name in df.columns:
        cleaned_name = col_name.replace(" ", "_").replace(",", "_").replace(";", "_") \
                               .replace("{", "_").replace("}", "_").replace("(", "_") \
                               .replace(")", "_").replace("\n", "_").replace("\t", "_") \
                               .replace("=", "_")
        df = df.withColumnRenamed(col_name, cleaned_name)
    return df

def load(file_path):
    """
    Loads data from a CSV file into a PySpark DataFrame, cleans column names,
    and saves it as a table.
    """
    spark = SparkSession.builder.appName("Load_Data").getOrCreate()
    print(f"Loading data from {file_path} into a Spark DataFrame...")
    
    # Load CSV into DataFrame
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    print(f"Data successfully loaded into a DataFrame with {df.count()} rows.")

    # Clean column names
    df = clean_column_names(df)

    # Persist the DataFrame as a table
    df.write.format("delta").mode("overwrite").saveAsTable("flight_delay_data")
    print("Data saved as a Delta table: flight_delay_data")

if __name__ == "__main__":
    file_path = "dbfs:/FileStore/flight_delays.csv"
    load(file_path)
