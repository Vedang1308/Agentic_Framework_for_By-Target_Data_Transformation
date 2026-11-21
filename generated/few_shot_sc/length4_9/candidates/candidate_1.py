import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the source date column to datetime
    # Format in sample: '1/2/2018 0:11'
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract calendar date for grouping and final output
    # Target format: '01/02/2018'
    df['cal_date'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour and map to target column names
    # 0 -> 12:00 AM, 1 -> 1:00 AM, ..., 11 -> 11:00 AM, 12 -> 12:00 PM, 13 -> 1:00 PM, ..., 23 -> 11:00 PM
    def map_hour_to_label(h):
        if h == 0:
            return '12:00 AM'
        elif h < 12:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else:
            return f'{h-12}:00 PM'
    
    df['hour_label'] = df['dt'].dt.hour.apply(map_hour_to_label)
    
    # 4. Aggregate values for each date and hour bucket
    # Using mean to handle multiple minutes per hour and ignore NaNs
    agg_df = df.groupby(['cal_date', 'hour_label'])['zone_016'].mean().reset_index()
    
    # 5. Pivot the data to wide format
    # Index: cal_date, Columns: hour_label, Values: zone_016
    pivot_df = agg_df.pivot(index='cal_date', columns='hour_label', values='zone_016')
    
    # 6. Rename columns to match target schema exactly
    # The pivot columns are already the correct labels ('1:00 AM', etc.)
    # But we need to ensure all 24 columns exist. If a date doesn't have data for an hour, it's NaN.
    
    # Reset index to make 'cal_date' a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'cal_date': 'date'})
    
    # 7. Define the exact target column order
    target_cols = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', 
        '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', 
        '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', 
        '12:00 AM'
    ]
    
    # 8. Ensure all target columns are present (filling missing ones with NaN if necessary)
    for col in target_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = pd.NA
            
    # 9. Select and return the final dataframe with exact column order
    return pivot_df[target_cols]