import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column to extract month
    source = source.copy()
    source['date_dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month_num'] = source['date_dt'].dt.month
    
    # 2. Define the mapping from source hour columns to 1-12 integer hours
    # Source columns are like "1:00 AM", "12:00 PM", etc.
    # We need to identify these columns. They are all float columns except DSL?
    # Actually, we can just list them or infer from names.
    # Let's create a mapping dictionary based on standard 12-hour clock names.
    
    hour_mapping = {}
    for h in range(1, 13):
        if h == 12:
            hour_mapping['12:00 AM'] = 12
            hour_mapping['12:00 PM'] = 12
        else:
            hour_mapping[f'{h}:00 AM'] = h
            hour_mapping[f'{h}:00 PM'] = h
            
    # Filter columns that are in our mapping
    valid_hour_cols = [col for col in source.columns if col in hour_mapping]
    
    # 3. Melt the DataFrame to long format
    # We keep 'month_num' for grouping. We don't strictly need 'date_dt' anymore.
    df_long = source.melt(
        id_vars=['month_num'],
        value_vars=valid_hour_cols,
        var_name='hour_label',
        value_name='value'
    )
    
    # 4. Map hour labels to integers 1-12
    df_long['hour'] = df_long['hour_label'].map(hour_mapping)
    
    # Drop rows where hour mapping failed (should be none if valid_hour_cols is correct)
    df_long = df_long.dropna(subset=['hour'])
    
    # 5. Group by hour and month, and calculate the mean
    # The target values look like averages (means) of the daily values for that hour in that month.
    grouped = df_long.groupby(['hour', 'month_num'])['value'].mean()
    
    # 6. Pivot the result to have months as columns
    # Unstack the month_num level to become columns
    df_pivot = grouped.unstack('month_num')
    
    # 7. Rename month columns to lowercase month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_pivot.columns = df_pivot.columns.map(month_names)
    
    # 8. Reset index to bring 'hour' back as a column
    df_result = df_pivot.reset_index()
    
    # 9. Ensure 'hour' is integer type
    df_result['hour'] = df_result['hour'].astype(int)
    
    # 10. Define target columns and select them
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # Sort by hour to match typical expected output order, though not strictly required if columns are selected
    df_result = df_result.sort_values('hour').reset_index(drop=True)
    
    return df_result[target_columns]