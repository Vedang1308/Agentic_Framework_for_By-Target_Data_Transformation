import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Define the target column names
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # 1. Parse the date column
    source = source.copy()
    source['date'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # 2. Identify hour columns (all columns except 'date' and 'DSL')
    hour_cols = [col for col in source.columns if col not in ['date', 'DSL']]
    
    # 3. Melt the dataframe to long format
    # id_vars=['date'], value_vars=hour_cols
    df_long = source.melt(id_vars=['date'], value_vars=hour_cols, var_name='hour_label', value_name='value')
    
    # 4. Map hour labels to 24-hour integer format
    # 12:00 AM -> 0, 1:00 AM -> 1, ..., 11:00 AM -> 11, 12:00 PM -> 12, 1:00 PM -> 13, ..., 11:00 PM -> 23
    def map_hour(label):
        label = label.strip()
        if 'AM' in label:
            hour = int(label.split(':')[0])
            if hour == 12:
                return 0
            else:
                return hour
        else: # PM
            hour = int(label.split(':')[0])
            if hour == 12:
                return 12
            else:
                return hour + 12
                
    df_long['hour'] = df_long['hour_label'].apply(map_hour)
    
    # 5. Extract month name from date
    # Map month number to lowercase name
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_long['month'] = df_long['date'].dt.month.map(month_map)
    
    # 6. Aggregate by hour and month
    # Calculate mean value for each hour-month combination
    df_agg = df_long.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 7. Pivot to wide format
    # Index: hour, Columns: month, Values: value
    df_pivot = df_agg.pivot(index='hour', columns='month', values='value')
    
    # 8. Reset index to make 'hour' a column
    df_pivot = df_pivot.reset_index()
    
    # 9. Ensure all month columns are present, even if empty (NaN)
    for month in month_map.values():
        if month not in df_pivot.columns:
            df_pivot[month] = np.nan
            
    # 10. Select and order columns as per target
    df_result = df_pivot[target_columns]
    
    # 11. Sort by hour for deterministic output (optional but good practice)
    df_result = df_result.sort_values('hour').reset_index(drop=True)
    
    return df_result