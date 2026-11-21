import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the exact target columns in the required order
    target_columns = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', 
        '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', 
        '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', 
        '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 1. Parse the source date column
    # Format: '%m/%d/%Y %H:%M'
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_key'] = df['datetime'].dt.normalize() # Floor to midnight of the same day
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map 24-hour integer to target column labels
    # 0 -> 12:00 AM, 1 -> 1:00 AM, ..., 12 -> 12:00 PM, ..., 23 -> 11:00 PM
    def map_hour_to_label(h):
        if h == 0:
            return '12:00 AM'
        elif h < 12:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else:
            return f'{h-12}:00 PM'
            
    df['hour_label'] = df['hour'].apply(map_hour_to_label)
    
    # 4. Aggregate values for each date and hour
    # We take the mean of the cooling_sp for each hour bucket
    grouped = df.groupby(['date_key', 'hour_label'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 5. Pivot the table
    # Index: date_key, Columns: hour_label, Values: zone_016_cooling_sp
    pivoted = grouped.pivot(index='date_key', columns='hour_label', values='zone_016_cooling_sp')
    
    # 6. Reset index to make date_key a column
    pivoted = pivoted.reset_index()
    
    # 7. Format the date column to '%m/%d/%Y'
    pivoted['date'] = pivoted['date_key'].dt.strftime('%m/%d/%Y')
    pivoted.drop(columns=['date_key'], inplace=True)
    
    # 8. Ensure all target hour columns exist (fill missing with NaN)
    # The pivot might not have all hours if they are completely missing from data
    for col in target_columns[1:]: # Skip 'date'
        if col not in pivoted.columns:
            pivoted[col] = pd.NA
            
    # 9. Select and order columns exactly as required
    result_df = pivoted[target_columns]
    
    # 10. Sort by date to ensure deterministic order (optional but good practice)
    # The target sample isn't strictly sorted, but usually tables are. 
    # However, to match exact schema, we just return the dataframe.
    # Let's convert types to float64 as per target schema
    for col in target_columns[1:]:
        result_df[col] = result_df[col].astype(float)
        
    return result_df