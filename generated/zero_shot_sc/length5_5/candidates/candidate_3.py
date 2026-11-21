import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing hourly (or sub-hourly) time series data
    into a daily summary DataFrame with 24 columns representing each hour of the day.
    """
    # 1. Parse the date column into datetime objects
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract the date (for grouping) and the hour (for pivoting)
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hours 0-23 to column names value1-value24
    # Hour 0 -> value1, Hour 1 -> value2, ..., Hour 23 -> value24
    df['value_col'] = 'value' + (df['hour'] + 1).astype(str)
    
    # 4. Pivot the data
    # Group by date_only and value_col, aggregating the 'zone_016_cooling_sp' values.
    # Using 'mean' to handle multiple entries per hour (e.g., 5-min intervals).
    pivot_df = df.pivot_table(
        index='date_only',
        columns='value_col',
        values='zone_016_cooling_sp',
        aggfunc='mean'
    )
    
    # 5. Reset index to make 'date_only' a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Rename 'date_only' to 'date'
    pivot_df = pivot_df.rename(columns={'date_only': 'date'})
    
    # 7. Format the date column to MM/DD/YYYY
    pivot_df['date'] = pivot_df['date'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 8. Define the target columns
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 9. Ensure all target columns exist (in case some hours are missing for all days)
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 10. Return the DataFrame with the correct columns
    return pivot_df[target_columns]