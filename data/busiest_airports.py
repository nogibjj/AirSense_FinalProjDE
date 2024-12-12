def create_busiest_airports_by_delays_table():
    """
    Creates a table of the busiest airports with the most delays.
    """
    query = """
    WITH DepartureData AS (
        SELECT 
            Origin_City AS City,
            SUM(Departure_Delay_Minutes) AS Total_Departure_Delay,
            COUNT(*) AS Total_Departures,
            ROUND(SUM(Departure_Delay_Minutes) / COUNT(*), 2) AS Avg_Departure_Delay
        FROM flight_delay_data
        WHERE Departure_Delay_Minutes > 0
        GROUP BY Origin_City
    ),
    ArrivalData AS (
        SELECT 
            Destination_City AS City,
            SUM(Arrival_Delay_Minutes) AS Total_Arrival_Delay,
            COUNT(*) AS Total_Arrivals,
            ROUND(SUM(Arrival_Delay_Minutes) / COUNT(*), 2) AS Avg_Arrival_Delay
        FROM flight_delay_data
        WHERE Arrival_Delay_Minutes > 0
        GROUP BY Destination_City
    )
    SELECT 
        COALESCE(d.City, a.City) AS City,
        COALESCE(d.Total_Departure_Delay, 0) AS Total_Departure_Delay,
        COALESCE(d.Total_Departures, 0) AS Total_Departures,
        COALESCE(d.Avg_Departure_Delay, 0) AS Avg_Departure_Delay,
        COALESCE(a.Total_Arrival_Delay, 0) AS Total_Arrival_Delay,
        COALESCE(a.Total_Arrivals, 0) AS Total_Arrivals,
        COALESCE(a.Avg_Arrival_Delay, 0) AS Avg_Arrival_Delay,
        ROUND(
            CAST(COALESCE(d.Avg_Departure_Delay, 0) AS DOUBLE) + 
            CAST(COALESCE(a.Avg_Arrival_Delay, 0) AS DOUBLE), 
            2
        ) AS Total_Avg_Delay
    FROM DepartureData d
    FULL OUTER JOIN ArrivalData a
    ON d.City = a.City
    ORDER BY Total_Avg_Delay DESC
    """
    busiest_airports = spark.sql(query)
    busiest_airports.write.format("delta").mode("overwrite").saveAsTable("busiest_airports_by_delays")
    print("busiest_airports_by_delays table created successfully.")


if __name__ == "__main__":
    create_busiest_airports_by_delays_table()