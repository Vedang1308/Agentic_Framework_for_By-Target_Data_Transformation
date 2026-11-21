import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source time-series data (10-min intervals) into daily hourly summaries.
    """
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.strftime('%m/%d/%Y')
    df['hour_24'] = df['datetime'].dt.hour
    
    # 3. Map 24-hour format to target column names (12-hour AM/PM)
    def map_hour_to_label(h):
        if h == 0:
            return '12:00 AM'
        elif h < 12:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else:
            return f'{h-12}:00 PM'
            
    df['hour_label'] = df['hour_24'].apply(map_hour_to_label)
    
    # 4. Aggregate data
    # Group by date and hour_label, then calculate the mean of cerc_logger_1
    # Using mean as it's the standard aggregation for sensor data over time intervals
    agg_df = df.groupby(['date_only', 'hour_label'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot the table
    # Rows: date_only, Columns: hour_label, Values: cerc_logger_1
    pivot_df = agg_df.pivot_table(index='date_only', columns='hour_label', values='cerc_logger_1')
    
    # 6. Define the exact target column order
    target_columns = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 7. Ensure all target columns exist (fill missing with NaN)
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 8. Select and order columns
    pivot_df = pivot_df[target_columns]
    
    # 9. Reset index to make 'date_only' a column named 'date'
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_only': 'date'})
    
    # 10. Final selection to ensure exact schema match
    final_columns = ['date'] + target_columns
    result_df = pivot_df[final_columns]
    
    return result_df