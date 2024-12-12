def create_delays_by_day_table():
    """
    Creates a table showing delays by day of the week.
    """
    query = """
    SELECT 
        DATE_FORMAT(Flight_Date, 'EEEE') AS Day_of_Week,
        ROUND(AVG(Departure_Delay_Minutes), 2) AS Avg_Departure_Delay,
        ROUND(AVG(Arrival_Delay_Minutes), 2) AS Avg_Arrival_Delay,
        COUNT(*) AS Total_Flights
    FROM flight_delay_data
    GROUP BY DATE_FORMAT(Flight_Date, 'EEEE')
    ORDER BY Total_Flights DESC
    """

    # Execute the query and create the table
    delays_by_day = spark.sql(query)
    delays_by_day.write.format("delta").mode("overwrite").saveAsTable("delays_by_day")
    print("Delays by day table created successfully.")

if __name__ == "__main__":
    create_delays_by_day_table()