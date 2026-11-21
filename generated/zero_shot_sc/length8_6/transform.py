import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms a source DataFrame with daily hourly data into a target DataFrame
    with monthly average hourly data.
    """
    # 1. Parse the date column
    source = source.copy()
    source['date_dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # 2. Extract month number and map to lowercase month name
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    source['month_name'] = source['date_dt'].dt.month.map(month_map)
    
    # 3. Identify hour columns (all columns except 'date', 'date_dt', 'month_name', 'DSL')
    # The hour columns are the ones with time strings.
    hour_cols = [col for col in source.columns if col not in ['date', 'date_dt', 'month_name', 'DSL']]
    
    # 4. Melt the DataFrame to long format
    df_long = source.melt(
        id_vars=['date_dt', 'month_name'],
        value_vars=hour_cols,
        var_name='hour_str',
        value_name='value'
    )
    
    # 5. Parse the hour string to extract the integer hour (1-12)
    # Format is "1:00 AM", "12:00 PM", etc.
    def extract_hour(hour_str):
        # Split by space to get "1:00" or "12:00"
        time_part = hour_str.split()[0]
        # Split by colon to get the hour number
        hour_num = int(time_part.split(':')[0])
        return hour_num
    
    df_long['hour'] = df_long['hour_str'].apply(extract_hour)
    
    # 6. Group by hour and month_name, and calculate the mean
    grouped = df_long.groupby(['hour', 'month_name'])['value'].mean()
    
    # 7. Unstack to pivot months into columns
    df_pivot = grouped.unstack('month_name')
    
    # 8. Ensure all months are present as columns
    all_months = ['january', 'february', 'march', 'april', 'may', 'june', 
                  'july', 'august', 'september', 'october', 'november', 'december']
    
    # Reindex columns to include all months, filling missing with NaN
    df_pivot = df_pivot.reindex(columns=all_months)
    
    # 9. Reset index to make 'hour' a column
    df_pivot = df_pivot.reset_index()
    
    # 10. Ensure hour is integer type
    df_pivot['hour'] = df_pivot['hour'].astype(int)
    
    # 11. Sort by hour for consistent output
    df_pivot = df_pivot.sort_values('hour').reset_index(drop=True)
    
    # 12. Define target columns
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    return df_pivot[target_columns]