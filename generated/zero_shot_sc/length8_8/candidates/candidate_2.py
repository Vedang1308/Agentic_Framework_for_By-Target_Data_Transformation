import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source daily hourly data into a monthly hourly summary.
    """
    # 1. Parse the date column to extract month
    source = source.copy()
    source['date'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month_num'] = source['date'].dt.month
    
    # 2. Melt the hour columns into long format
    # Identify hour columns
    hour_cols = [col for col in source.columns if col.startswith('Hour ')]
    
    # Melt
    df_long = pd.melt(
        source, 
        id_vars=['month_num'], 
        value_vars=hour_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # Extract hour number from 'Hour X' string
    df_long['hour'] = df_long['hour_col'].str.replace('Hour ', '').astype(int)
    df_long = df_long.drop(columns=['hour_col'])
    
    # 3. Map month numbers to lowercase month names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_long['month_name'] = df_long['month_num'].map(month_map)
    
    # 4. Aggregate by hour and month
    # Calculate the mean value for each hour in each month
    df_agg = df_long.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 5. Pivot to wide format
    # Index: hour, Columns: month_name, Values: value
    df_pivot = df_agg.pivot(index='hour', columns='month_name', values='value')
    
    # 6. Reset index to make hour a column
    df_pivot = df_pivot.reset_index()
    
    # 7. Ensure correct column order for months (Calendar order)
    target_months = [
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Ensure all target month columns exist, filling with NaN if missing
    for m in target_months:
        if m not in df_pivot.columns:
            df_pivot[m] = np.nan
            
    # 8. Sort rows by hour as string to match target sample order (1, 10, 11...)
    # The target sample shows order: 1, 10, 11, 12, 6, 7, 8, 9
    # This corresponds to a string sort of the hour values.
    df_pivot['hour_str'] = df_pivot['hour'].astype(str)
    df_pivot = df_pivot.sort_values('hour_str')
    df_pivot = df_pivot.drop(columns=['hour_str'])
    
    # 9. Final column selection and naming
    target_columns = ['hour'] + target_months
    
    # Ensure hour is int64
    df_pivot['hour'] = df_pivot['hour'].astype(int)
    
    df = df_pivot[target_columns]
    
    return df