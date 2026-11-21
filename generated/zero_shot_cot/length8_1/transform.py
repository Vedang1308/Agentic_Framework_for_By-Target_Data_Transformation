import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by pivoting
    sensor readings by Hour and Month.
    """
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['datetime'].dt.hour
    df['Month'] = df['datetime'].dt.month
    
    # 3. Map Month numbers to names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['Month_Name'] = df['Month'].map(month_map)
    
    # 4. Pivot the table
    # Index: Hour, Columns: Month_Name, Values: cerc_logger_1
    # Aggregation: mean (standard for time-series sensor data)
    pivot_df = df.pivot_table(
        index='Hour', 
        columns='Month_Name', 
        values='cerc_logger_1', 
        aggfunc='mean'
    )
    
    # 5. Ensure all 24 hours are present and sorted
    all_hours = pd.RangeIndex(0, 24)
    pivot_df = pivot_df.reindex(all_hours)
    
    # 6. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Rename the index column to 'Hour' if it was renamed during reset
    # (pivot_table usually keeps the name 'Hour' from the index)
    pivot_df = pivot_df.rename(columns={'index': 'Hour'})
    
    # 8. Define target columns
    target_columns = [
        'Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # 9. Ensure column order and existence
    # The pivot columns should already be the month names. 
    # We select them in the specific order required.
    result_df = pivot_df[target_columns]
    
    # 10. Ensure correct data types
    result_df['Hour'] = result_df['Hour'].astype(int)
    for col in target_columns[1:]:
        result_df[col] = result_df[col].astype(float)
        
    return result_df