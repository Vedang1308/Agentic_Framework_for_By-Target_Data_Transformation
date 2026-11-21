import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 2. Set Date as index for time-series operations
    df = df.set_index('Date')
    
    # 3. Sort by date to ensure chronological order
    df = df.sort_index()
    
    # 4. Create a complete daily date range from min to max date in source
    # This handles the case where one day is missing (182 -> 183 rows)
    full_date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    
    # 5. Reindex the dataframe to include all days in the range
    df = df.reindex(full_date_range)
    
    # 6. Interpolate missing values for the missing day(s)
    # Using method='time' is robust for datetime indices
    df = df.interpolate(method='time')
    
    # 7. Format the Date index back to string format '%m/%d/%Y'
    df.index = df.index.strftime('%m/%d/%Y')
    
    # 8. Reset index to make Date a column again
    df = df.reset_index()
    
    # 9. Rename columns from 1..24 to Hr 1..Hr 24
    rename_map = {str(i): f'Hr {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_map)
    
    # 10. Define target columns
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 11. Ensure only target columns are returned in correct order
    return df[target_columns]