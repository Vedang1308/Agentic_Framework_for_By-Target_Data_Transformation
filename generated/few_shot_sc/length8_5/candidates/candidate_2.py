import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # 1. Select relevant columns and melt the hourly value columns
    # We need 'date' and value1..value24
    value_cols = [f'value{i}' for i in range(1, 25)]
    df_melt = source[['date'] + value_cols].melt(
        id_vars=['date'],
        value_vars=value_cols,
        var_name='hour_col',
        value_name='value'
    )
    
    # 2. Extract hour number from the column name (e.g., 'value1' -> 1)
    df_melt['hour'] = df_melt['hour_col'].str.replace('value', '', regex=False).astype(int)
    
    # 3. Parse date and extract month
    df_melt['date_dt'] = pd.to_datetime(df_melt['date'], format='%m/%d/%Y')
    df_melt['month'] = df_melt['date_dt'].dt.month
    
    # 4. Aggregate by hour and month (calculate mean)
    # The target sample shows averages (e.g., for July, hour 1 is ~0.97, which looks like an average of the few July days provided)
    df_agg = df_melt.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 5. Pivot to get months as columns
    df_pivot = df_agg.pivot(index='hour', columns='month', values='value')
    
    # 6. Rename month columns to match target schema
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_pivot.rename(columns=month_names, inplace=True)
    
    # 7. Reset index to make 'hour' a column
    df_result = df_pivot.reset_index()
    
    # 8. Ensure all month columns exist (fill NaN if a month is missing entirely)
    # The target schema requires all month columns. Pivot might miss columns if no data exists.
    # We need to ensure the columns are in the specific order.
    target_month_cols = ['january', 'february', 'march', 'april', 'may', 'june', 
                         'july', 'august', 'september', 'october', 'november', 'december']
    
    # Add missing month columns with NaN if they don't exist
    for col in target_month_cols:
        if col not in df_result.columns:
            df_result[col] = pd.NA
            
    # 9. Select and order columns exactly as per target
    target_columns = ['hour'] + target_month_cols
    
    # Sort by hour for deterministic output (optional but good practice)
    df_result = df_result.sort_values(by='hour').reset_index(drop=True)
    
    return df_result[target_columns]