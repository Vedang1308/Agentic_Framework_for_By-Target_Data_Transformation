import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the target column names in the exact order required
    target_columns = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 1. Parse the source date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Create mapping from hour (0-23) to target column name
    hour_to_col = {
        0: '12:00 AM', 1: '1:00 AM', 2: '2:00 AM', 3: '3:00 AM', 
        4: '4:00 AM', 5: '5:00 AM', 6: '6:00 AM', 7: '7:00 AM', 
        8: '8:00 AM', 9: '9:00 AM', 10: '10:00 AM', 11: '11:00 AM',
        12: '12:00 PM', 13: '1:00 PM', 14: '2:00 PM', 15: '3:00 PM', 
        16: '4:00 PM', 17: '5:00 PM', 18: '6:00 PM', 19: '7:00 PM', 
        20: '8:00 PM', 21: '9:00 PM', 22: '10:00 PM', 23: '11:00 PM'
    }
    
    # Map hours to column names
    df['hour_col'] = df['hour'].map(hour_to_col)
    
    # 4. Aggregate: Mean of zone_016 per date and hour
    agg_df = df.groupby(['date_only', 'hour_col'])['zone_016'].mean().reset_index()
    
    # 5. Pivot the data
    pivot_df = agg_df.pivot(index='date_only', columns='hour_col', values='zone_016')
    
    # 6. Ensure all target hour columns exist and are in the correct order
    # Extract the hour columns from the target_columns list (excluding 'date')
    hour_cols = target_columns[1:]
    
    # Reindex to ensure all columns are present, filling missing with NaN
    pivot_df = pivot_df.reindex(columns=hour_cols)
    
    # 7. Format the date index to string '%m/%d/%Y'
    pivot_df.index = pivot_df.index.map(lambda x: x.strftime('%m/%d/%Y'))
    
    # 8. Reset index to make date a column
    pivot_df = pivot_df.reset_index()
    
    # 9. Rename the date column to match target exactly
    pivot_df = pivot_df.rename(columns={'date_only': 'date'})
    
    # 10. Select and order columns exactly as per target schema
    result_df = pivot_df[target_columns]
    
    return result_df