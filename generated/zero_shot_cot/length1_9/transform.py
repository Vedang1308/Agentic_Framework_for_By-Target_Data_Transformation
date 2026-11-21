import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hour to target column names (1:00 to 24:00)
    # Hour 0 -> 1:00, Hour 1 -> 2:00, ..., Hour 23 -> 24:00
    df['hour_label'] = df['hour'].apply(lambda h: f"{h+1}:00")
    
    # 4. Aggregate by date and hour_label
    # Based on analysis, the aggregation is SUM because target values (~4000) 
    # are roughly 60x the source minute values (~67).
    grouped = df.groupby(['date_only', 'hour_label'])['zone_016'].sum().reset_index()
    
    # 5. Pivot the data
    # Index: date_only, Columns: hour_label, Values: zone_016
    pivoted = grouped.pivot_table(index='date_only', columns='hour_label', values='zone_016', aggfunc='sum')
    
    # 6. Fill missing values with 0
    pivoted = pivoted.fillna(0)
    
    # 7. Ensure all expected hour columns exist and are in order
    expected_hours = [f"{h}:00" for h in range(1, 25)]
    
    # Reindex columns to ensure all hours are present and in correct order
    pivoted = pivoted.reindex(columns=expected_hours, fill_value=0)
    
    # 8. Format the date index to 'cst' format: '%a %m/%d/%Y'
    # Convert date_only back to datetime for formatting, then to string
    pivoted.index = pd.to_datetime(pivoted.index)
    pivoted.index = pivoted.index.strftime('%a %m/%d/%Y')
    
    # 9. Reset index to make 'cst' a column
    pivoted = pivoted.reset_index()
    pivoted = pivoted.rename(columns={'index': 'cst'})
    
    # 10. Define target columns
    target_columns = ['cst'] + expected_hours
    
    # 11. Return the final dataframe with exact column names
    return pivoted[target_columns]