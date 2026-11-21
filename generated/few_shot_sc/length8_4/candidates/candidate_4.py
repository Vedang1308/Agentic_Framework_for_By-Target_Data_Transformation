import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Identify the 24 hourly columns
    hourly_cols = [f'PCT_HOURLY_{i:02d}00' for i in range(1, 25)]
    
    # 2. Melt the dataframe from wide to long format
    # We keep DT_STRATA as an identifier, and melt the hourly columns
    df_long = pd.melt(
        df, 
        id_vars=['DT_STRATA'], 
        value_vars=hourly_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # 3. Extract hour number from the column name
    # e.g., 'PCT_HOURLY_0100' -> '01' -> 1
    df_long['hour'] = df_long['hour_col'].str.replace('PCT_HOURLY_', '').str.replace('00', '').astype(int)
    
    # 4. Parse date and extract month
    dt_parsed = pd.to_datetime(df_long['DT_STRATA'])
    df_long['month_num'] = dt_parsed.dt.month
    
    # 5. Map month number to lowercase month name
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_long['month_name'] = df_long['month_num'].map(month_map)
    
    # 6. Aggregate: Group by hour and month, calculate mean
    # This reduces the data to one row per hour per month
    df_agg = df_long.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 7. Pivot to wide format: hours as rows, months as columns
    df_pivot = df_agg.pivot(index='hour', columns='month_name', values='value')
    
    # 8. Reset index to make 'hour' a column again
    df_result = df_pivot.reset_index()
    
    # 9. Ensure hour is integer type
    df_result['hour'] = df_result['hour'].astype(int)
    
    # 10. Define target columns in the exact order required
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # 11. Sort by hour to ensure 1-24 order
    df_result = df_result.sort_values('hour').reset_index(drop=True)
    
    # 12. Select and return only the target columns
    # Note: If a month is missing in the data, it will be NaN, which is acceptable behavior for aggregation
    return df_result[target_columns]