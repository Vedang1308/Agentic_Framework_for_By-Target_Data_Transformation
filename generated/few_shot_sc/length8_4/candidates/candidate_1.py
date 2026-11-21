import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse dates to extract month
    df['datetime'] = pd.to_datetime(df['DT_STRATA'])
    df['month'] = df['datetime'].dt.month
    
    # 2. Identify hourly columns to melt (0100 to 2400)
    hourly_cols = [f'PCT_HOURLY_{i:02d}00' for i in range(1, 25)]
    
    # 3. Melt the DataFrame to long format
    # We only need datetime (for month) and the hourly values
    df_long = df[['datetime', 'month'] + hourly_cols].melt(
        id_vars=['datetime', 'month'], 
        value_vars=hourly_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # 4. Extract hour integer from column name (e.g., 'PCT_HOURLY_0100' -> 1)
    df_long['hour'] = df_long['hour_col'].str.extract(r'(\d{2})').astype(int)
    
    # 5. Group by hour and month, and calculate the mean
    # The target values appear to be averages of the daily profiles for that hour/month
    aggregated = df_long.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 6. Pivot to wide format: hours as index, months as columns
    df_wide = aggregated.pivot_table(index='hour', columns='month', values='value')
    
    # 7. Rename month columns to lowercase month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_wide = df_wide.rename(columns=month_names)
    
    # 8. Reset index to make 'hour' a column and ensure integer type
    df_wide = df_wide.reset_index()
    df_wide['hour'] = df_wide['hour'].astype(int)
    
    # 9. Define target columns in verbatim order
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # 10. Return the DataFrame with exact column order
    return df_wide[target_columns]