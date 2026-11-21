import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    Source: date, zone_016_cooling_sp
    Target: Date, Hr 1 ... Hr 24
    """
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    # The target Date format is %m/%d/%Y
    df['Date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    # The target hours are 1-24, corresponding to 0-23 in 24-hour clock
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Aggregate data for each Date and Hour
    # We use 'mean' to aggregate multiple entries within the same hour.
    # If the value is constant (as in the sample), mean equals the value.
    # If there are missing hours, they won't appear in the groupby, resulting in NaN after pivot.
    aggregated = df.groupby(['Date', 'hour'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 4. Pivot the table to have hours as columns
    # Index: Date, Columns: hour, Values: zone_016_cooling_sp
    pivoted = aggregated.pivot(index='Date', columns='hour', values='zone_016_cooling_sp')
    
    # 5. Ensure all 24 hours are present as columns (0-23)
    # If a specific hour is missing for a date, it will be NaN.
    all_hours = list(range(24))
    pivoted = pivoted.reindex(columns=all_hours)
    
    # 6. Rename columns to match target schema: Hr 1, Hr 2, ..., Hr 24
    # Map 0 -> 'Hr 1', 1 -> 'Hr 2', etc.
    pivoted.columns = [f'Hr {i+1}' for i in all_hours]
    
    # 7. Reset index to make 'Date' a column
    pivoted = pivoted.reset_index()
    
    # 8. Define the target column order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 9. Select and return the final dataframe with exact column names
    df_final = pivoted[target_columns]
    
    return df_final