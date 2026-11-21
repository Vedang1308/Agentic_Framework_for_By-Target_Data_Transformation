import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    # Source format is '%m/%d/%Y %H:%M' e.g., '7/28/2019 4:50'
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date string for grouping and final output
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour integer (0-23)
    df['hour_int'] = df['datetime'].dt.hour
    
    # 4. Map hour integer to target column names (12-hour AM/PM format)
    def map_hour_to_col(h):
        if h == 0:
            return '12:00 AM'
        elif h == 12:
            return '12:00 PM'
        elif h < 12:
            return f'{h}:00 AM'
        else:
            return f'{h - 12}:00 PM'
            
    df['hour_col'] = df['hour_int'].apply(map_hour_to_col)
    
    # 5. Group by date and hour column, aggregate mean of cerc_logger_1
    # This reduces the 10-minute intervals to hourly averages
    grouped = df.groupby(['date_str', 'hour_col'])['cerc_logger_1'].mean().reset_index()
    
    # 6. Pivot the table to wide format
    # Index: date_str, Columns: hour_col, Values: cerc_logger_1
    pivoted = grouped.pivot(index='date_str', columns='hour_col', values='cerc_logger_1')
    
    # 7. Reset index to make date_str a column named 'date'
    pivoted = pivoted.reset_index()
    pivoted = pivoted.rename(columns={'date_str': 'date'})
    
    # 8. Define the exact target column order
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', 
        '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 9. Ensure all columns exist (in case some hours are missing for some days)
    # Pivot might not have all hours if data is sparse, but we need the schema to match.
    # We select the columns; if any are missing, pandas will raise KeyError unless we handle it.
    # However, based on the problem description, we assume standard hourly data coverage or 
    # that we just return what we have in that specific order. 
    # To be safe against missing columns in pivot result, we can reindex.
    
    # Reindex to ensure all target columns are present, filling missing with NaN
    pivoted = pivoted.reindex(columns=target_columns)
    
    return pivoted[target_columns]