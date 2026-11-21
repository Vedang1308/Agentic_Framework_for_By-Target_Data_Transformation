import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Identify hourly columns. They are all columns except 'date' and 'DSL'.
    # The source schema lists: date, 1:00 AM ... 12:00 PM, DSL
    # We can filter columns that are not 'date' and not 'DSL'
    hour_cols = [col for col in source.columns if col not in ['date', 'DSL']]
    
    # 2. Melt the dataframe to long format
    df = source.copy()
    df_melted = df.melt(
        id_vars=['date'], 
        value_vars=hour_cols, 
        var_name='hour_label', 
        value_name='value'
    )
    
    # 3. Parse date to extract month
    df_melted['date_dt'] = pd.to_datetime(df_melted['date'])
    df_melted['month'] = df_melted['date_dt'].dt.month
    
    # 4. Map hour labels to integers 1-24
    # Mapping:
    # 12:00 AM -> 1
    # 1:00 AM -> 2
    # ...
    # 11:00 AM -> 12
    # 12:00 PM -> 13
    # 1:00 PM -> 14
    # ...
    # 11:00 PM -> 24
    
    hour_map = {}
    # AM hours
    for h in range(1, 12):
        hour_map[f'{h}:00 AM'] = h + 1
    hour_map['12:00 AM'] = 1
    
    # PM hours
    hour_map['12:00 PM'] = 13
    for h in range(1, 12):
        hour_map[f'{h}:00 PM'] = h + 12
        
    df_melted['hour'] = df_melted['hour_label'].map(hour_map)
    
    # 5. Group by hour and month, calculate mean
    # The target values look like averages of the daily values for that hour in that month.
    grouped = df_melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 6. Pivot to wide format
    # Rows: hour
    # Columns: month
    # Values: mean value
    df_pivot = grouped.pivot(index='hour', columns='month', values='value')
    
    # 7. Map month numbers to names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    df_pivot.columns = [month_names[col] for col in df_pivot.columns]
    
    # 8. Reset index to make 'hour' a column
    df_pivot = df_pivot.reset_index()
    
    # 9. Ensure hour is integer
    df_pivot['hour'] = df_pivot['hour'].astype(int)
    
    # 10. Define target columns in correct order
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # 11. Select and return
    # Note: If some months are missing in the data, they will be NaN, which is expected.
    return df_pivot[target_columns]