import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse datetime
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string in target format
    df['date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour
    df['hour'] = df['datetime'].dt.hour
    
    # 4. Map hour to target column names
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
    
    # 5. Aggregate (mean) by date and hour label
    # Group by date and hour_label, take mean of cerc_logger_1
    df_agg = df.groupby(['date', 'hour_label'])['cerc_logger_1'].mean().reset_index()
    
    # 6. Pivot to wide format
    df_pivot = df_agg.pivot(index='date', columns='hour_label', values='cerc_logger_1')
    
    # 7. Reset index to make 'date' a column again
    df_pivot = df_pivot.reset_index()
    
    # 8. Define the exact target column order
    target_hour_cols = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM',
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM',
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    target_columns = ['date'] + target_hour_cols
    
    # 9. Ensure all target columns exist (fill with NaN if an hour is missing for a day)
    for col in target_hour_cols:
        if col not in df_pivot.columns:
            df_pivot[col] = np.nan
            
    # 10. Select and order columns
    return df_pivot[target_columns]