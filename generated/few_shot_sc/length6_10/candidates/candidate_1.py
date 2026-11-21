import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse datetime
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract Date and Hour
    # Target 'Date' is just the date part formatted as MM/DD/YYYY
    df['Date'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # Target Hours are 1-24. 
    # Standard hour 0 (12am-1am) maps to Hr 1.
    # Standard hour 23 (11pm-12am) maps to Hr 24.
    df['Hour'] = df['dt'].dt.hour + 1
    
    # 3. Pivot the data
    # Group by Date and Hour, aggregate values. 
    # Using mean() to handle multiple 5-min intervals per hour.
    # If there's only one value, mean is that value.
    pivoted = df.pivot_table(
        index='Date', 
        columns='Hour', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 4. Format columns
    # Rename columns from integers to 'Hr X'
    pivoted.columns = [f'Hr {col}' for col in pivoted.columns]
    
    # 5. Reset index to make Date a column
    pivoted = pivoted.reset_index()
    
    # 6. Ensure all Hr 1 to Hr 24 columns exist and are in order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # Reindex columns to ensure missing hours are NaN and order is correct
    pivoted = pivoted.reindex(columns=target_columns)
    
    # 7. Return final dataframe
    return pivoted[target_columns]