import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse dates and extract month names
    df['DT_STRATA'] = pd.to_datetime(df['DT_STRATA'])
    df['month'] = df['DT_STRATA'].dt.month_name().str.lower()
    
    # 2. Identify hourly columns (excluding 2500 which is not in target)
    hourly_cols = [col for col in df.columns if col.startswith('PCT_HOURLY_') and col != 'PCT_HOURLY_2500']
    
    # 3. Melt the dataframe to long format
    # We keep 'month' as an id variable. The other columns become 'variable' and 'value'.
    melted = df.melt(id_vars=['month'], value_vars=hourly_cols, var_name='hour_col', value_name='value')
    
    # 4. Extract hour number from column name
    # Column names are like 'PCT_HOURLY_0100'. We want the hour part (01 -> 1).
    # The pattern is PCT_HOURLY_XX00. XX is the hour.
    melted['hour'] = melted['hour_col'].str.extract(r'PCT_HOURLY_(\d{2})00').astype(int)
    
    # 5. Aggregate by hour and month
    # The target values appear to be averages of the daily values for that hour/month combination.
    aggregated = melted.groupby(['hour', 'month'])['value'].mean()
    
    # 6. Pivot to wide format: rows=hour, columns=month
    pivot_df = aggregated.unstack(level='month')
    
    # 7. Reset index to make 'hour' a column
    pivot_df = pivot_df.reset_index()
    
    # 8. Ensure column order and names match target
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # Check if all target month columns exist, fill with NaN if not (though unlikely with full data)
    for col in target_columns[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = float('nan')
            
    # Select and order columns
    result_df = pivot_df[target_columns]
    
    # Sort by hour to match the expected output order (1-24)
    result_df = result_df.sort_values('hour').reset_index(drop=True)
    
    return result_df