from pyspark.sql import SparkSession

def create_airlines_performance_table():
    """
    Creates a table ranking airlines by on-time performance.
    """
    spark = SparkSession.builder.appName("Airline Performance").getOrCreate()

    # SQL query to calculate average delays for each airline
    query = """
    SELECT 
        Airline_Name,
        ROUND(AVG(Departure_Delay_Minutes), 2) AS Avg_Departure_Delay,
        ROUND(AVG(Arrival_Delay_Minutes), 2) AS Avg_Arrival_Delay,
        COUNT(*) AS Total_Flights
    FROM flight_delay_data
    GROUP BY Airline_Name
    ORDER BY Avg_Arrival_Delay ASC, Avg_Departure_Delay ASC
    """

    # Execute the query and create the table
    airline_performance = spark.sql(query)
    airline_performance.write.format("delta").mode("overwrite").saveAsTable("airline_performance")
    print("Airline performance table created successfully.")

if __name__ == "__main__":
    create_airlines_performance_table()
