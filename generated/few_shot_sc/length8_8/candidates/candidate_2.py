import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse date and extract month name
    df['date_dt'] = pd.to_datetime(df['date'])
    df['month'] = df['date_dt'].dt.strftime('%B').str.lower()
    
    # 2. Identify hour columns
    hour_cols = [col for col in df.columns if col.startswith('Hour')]
    
    # 3. Melt the dataframe to long format
    # We keep 'date_dt' and 'month' as id_vars to track the month for each value
    long_df = pd.melt(
        df, 
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # 4. Extract integer hour from column name (e.g., "Hour 1" -> 1)
    long_df['hour'] = long_df['hour_col'].str.replace('Hour ', '').astype(int)
    
    # 5. Aggregate by hour and month
    # Calculate the mean value for each hour in each month
    agg_df = long_df.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 6. Pivot to wide format: index=hour, columns=month, values=value
    pivoted_df = agg_df.pivot(index='hour', columns='month', values='value')
    
    # 7. Reset index to make 'hour' a column
    pivoted_df = pivoted_df.reset_index()
    
    # 8. Define target columns
    target_months = [
        'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    target_columns = ['hour'] + target_months
    
    # 9. Ensure all month columns exist (fill missing with NaN if a month has no data)
    for m in target_months:
        if m not in pivoted_df.columns:
            pivoted_df[m] = pd.NA
            
    # 10. Select and order columns verbatim
    result_df = pivoted_df[target_columns]
    
    # 11. Sort by hour numerically for deterministic output
    result_df = result_df.sort_values(by='hour').reset_index(drop=True)
    
    return result_df