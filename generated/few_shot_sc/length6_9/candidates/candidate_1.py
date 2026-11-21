import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms high-frequency time series data into daily hourly aggregates.
    
    Steps:
    1. Parse the 'date' column to datetime.
    2. Extract the calendar date and the hour of the day.
    3. Group by calendar date and hour, then aggregate (mean) the 'zone_016' values.
    4. Pivot the data so hours become columns.
    5. Map hours 0-23 to columns 'Hr 1'-'Hr 24'.
    6. Format the date column and select final columns.
    """
    df = source.copy()
    
    # 1. Parse datetime
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract components
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Group by date and hour, aggregate mean of zone_016
    # We dropna on the value column to ensure valid aggregation
    grouped = df.groupby(['date_only', 'hour'])['zone_016'].mean()
    
    # 4. Unstack to pivot hours into columns
    # This results in a DataFrame with index=date_only, columns=hour (0-23)
    df_pivoted = grouped.unstack(level='hour', fill_value=None)
    
    # 5. Rename columns from 0-23 to 'Hr 1'-'Hr 24'
    # Hour 0 -> Hr 1, Hour 1 -> Hr 2, ..., Hour 23 -> Hr 24
    rename_map = {h: f'Hr {h+1}' for h in range(24)}
    df_pivoted = df_pivoted.rename(columns=rename_map)
    
    # Ensure all 24 hour columns exist, even if empty for some dates
    for h in range(24):
        col_name = f'Hr {h+1}'
        if col_name not in df_pivoted.columns:
            df_pivoted[col_name] = float('nan')
            
    # 6. Reset index to make 'date_only' a column
    df_pivoted = df_pivoted.reset_index()
    
    # Format date column as MM/DD/YYYY
    df_pivoted['Date'] = pd.to_datetime(df_pivoted['date_only']).dt.strftime('%m/%d/%Y')
    
    # Drop the temporary date_only column if it persists (reset_index creates it as a column)
    if 'date_only' in df_pivoted.columns:
        df_pivoted = df_pivoted.drop(columns=['date_only'])
        
    # Define target columns verbatim
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # Select and order columns
    result = df_pivoted[target_columns]
    
    return result