import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse dates to extract month
    df = source.copy()
    df['date'] = pd.to_datetime(df['DT_STRATA'])
    df['month_num'] = df['date'].dt.month
    
    # 2. Identify hourly columns (1 to 24)
    # Columns are named PCT_HOURLY_0100 ... PCT_HOURLY_2400
    hourly_cols = [f'PCT_HOURLY_{i:02d}00' for i in range(1, 25)]
    
    # 3. Melt the dataframe to long format
    # We only need the date-derived month and the hourly values
    melt_cols = ['month_num'] + hourly_cols
    df_melted = df[melt_cols].melt(
        id_vars=['month_num'], 
        value_vars=hourly_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # 4. Extract hour integer from column name
    # e.g., 'PCT_HOURLY_0100' -> 1
    df_melted['hour'] = df_melted['hour_col'].str.extract(r'(\d{2})').astype(int)
    
    # 5. Aggregate: Mean value for each hour and month
    aggregated = df_melted.groupby(['hour', 'month_num'])['value'].mean().reset_index()
    
    # 6. Pivot to wide format: rows=hour, columns=month, values=mean
    pivoted = aggregated.pivot(index='hour', columns='month_num', values='value')
    
    # 7. Rename month columns to lowercase names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivoted = pivoted.rename(columns=month_map)
    
    # 8. Reset index to make 'hour' a column
    result = pivoted.reset_index()
    
    # 9. Ensure column order and types
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # Sort by hour just in case
    result = result.sort_values('hour').reset_index(drop=True)
    
    # Ensure hour is int
    result['hour'] = result['hour'].astype(int)
    
    return result[target_columns]