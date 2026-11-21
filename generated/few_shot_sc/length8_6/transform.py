import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Identify hour columns (exclude 'date' and 'DSL')
    hour_cols = [col for col in source.columns if col not in ['date', 'DSL']]
    
    # 2. Melt the dataframe to long format
    df_long = source.melt(
        id_vars=['date'], 
        value_vars=hour_cols, 
        var_name='hour_label', 
        value_name='value'
    )
    
    # 3. Parse hour_label to integer hour (1-24)
    # Mapping logic:
    # 12:00 AM -> 24
    # 1:00 AM -> 1 ... 11:00 AM -> 11
    # 12:00 PM -> 12
    # 1:00 PM -> 13 ... 11:00 PM -> 23
    def parse_hour(label):
        label = label.strip()
        period = label.split(' ')[1] # 'AM' or 'PM'
        hour_str = label.split(':')[0]
        h = int(hour_str)
        
        if period == 'AM':
            if h == 12:
                return 24
            else:
                return h
        else: # PM
            if h == 12:
                return 12
            else:
                return h + 12
                
    df_long['hour'] = df_long['hour_label'].apply(parse_hour)
    
    # 4. Parse date to extract month
    df_long['date_parsed'] = pd.to_datetime(df_long['date'])
    df_long['month'] = df_long['date_parsed'].dt.month
    
    # 5. Group by hour and month, calculate mean
    grouped = df_long.groupby(['hour', 'month'])['value'].mean()
    
    # 6. Pivot to wide format
    # Index: hour, Columns: month, Values: mean
    df_pivot = grouped.unstack(fill_value=np.nan)
    
    # 7. Rename month columns to lowercase month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_pivot = df_pivot.rename(columns=month_names)
    
    # 8. Reset index to make 'hour' a column
    df_result = df_pivot.reset_index()
    
    # 9. Sort by hour
    df_result = df_result.sort_values('hour').reset_index(drop=True)
    
    # 10. Define target columns
    target_columns = ['hour'] + [
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Ensure all target columns exist (in case some months are missing in data)
    for col in target_columns:
        if col not in df_result.columns:
            df_result[col] = np.nan
            
    return df_result[target_columns]