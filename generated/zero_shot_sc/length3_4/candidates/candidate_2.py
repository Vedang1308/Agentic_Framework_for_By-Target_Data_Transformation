import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from long format (timestamp, value) 
    to wide format (date, Hour 1..24).
    """
    # 1. Parse the date column to datetime
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract the date part as string in target format
    df['date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract the hour part and map to target column names
    # Hour 0 -> Hour 1, Hour 1 -> Hour 2, ..., Hour 23 -> Hour 24
    df['hour_col'] = 'Hour ' + (df['datetime'].dt.hour + 1).astype(str)
    
    # 4. Pivot the table
    # Use pivot_table to handle potential duplicates (multiple readings per hour)
    # aggfunc='first' takes the first reading for that hour
    df_pivot = df.pivot_table(
        index='date', 
        columns='hour_col', 
        values='zone_016_cooling_sp', 
        aggfunc='first'
    )
    
    # 5. Define the expected target columns
    target_hours = [f'Hour {i}' for i in range(1, 25)]
    target_columns = ['date'] + target_hours
    
    # 6. Ensure all hour columns are present, filling missing ones with NaN
    # Reindexing the columns ensures the order and presence of all 24 hours
    df_pivot = df_pivot.reindex(columns=target_hours)
    
    # 7. Reset index to make 'date' a column again
    df_pivot = df_pivot.reset_index()
    
    # 8. Ensure the final column order matches the target exactly
    df_result = df_pivot[target_columns]
    
    return df_result