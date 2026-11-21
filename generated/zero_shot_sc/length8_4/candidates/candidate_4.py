import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column to extract the month
    source = source.copy()
    source['DT_STRATA'] = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    source['month_num'] = source['DT_STRATA'].dt.month
    
    # 2. Map month numbers to target column names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    source['month_name'] = source['month_num'].map(month_map)
    
    # 3. Identify hourly columns to melt
    # Columns are PCT_HOURLY_0100 to PCT_HOURLY_2400
    # We exclude PCT_HOURLY_2500 as it's not in the target hours 1-24
    hourly_cols = [col for col in source.columns if col.startswith('PCT_HOURLY_') and col != 'PCT_HOURLY_2500']
    
    # 4. Melt the dataframe
    # id_vars: keep month_name (and potentially Strata_ID if we needed it, but we aggregate globally)
    # value_vars: the hourly columns
    # var_name: 'hour_col', value_name: 'value'
    melted = source.melt(
        id_vars=['month_name'], 
        value_vars=hourly_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # 5. Extract hour number from column name
    # Format is PCT_HOURLY_HH00. e.g., 0100 -> 1, 2400 -> 24
    melted['hour'] = melted['hour_col'].apply(lambda x: int(x.split('_')[-1]) // 100)
    
    # 6. Aggregate by hour and month
    # We take the mean of the values for each hour-month combination
    aggregated = melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 7. Pivot to wide format
    # Index: hour, Columns: month_name, Values: value
    pivoted = aggregated.pivot(index='hour', columns='month_name', values='value')
    
    # 8. Clean up and format
    pivoted = pivoted.reset_index()
    
    # Ensure all month columns exist and are in the correct order
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # Fill NaN with 0 if any month/hour combination is missing
    pivoted = pivoted.fillna(0)
    
    # Select and order columns
    # Note: pivot might reorder columns alphabetically or by appearance. We must enforce order.
    # Also ensure 'hour' is the first column.
    
    # Check if all target columns exist in pivoted
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = 0
            
    df = pivoted[target_columns]
    
    # Ensure hour is integer
    df['hour'] = df['hour'].astype(int)
    
    # Sort by hour to match target structure
    df = df.sort_values('hour').reset_index(drop=True)
    
    return df[target_columns]