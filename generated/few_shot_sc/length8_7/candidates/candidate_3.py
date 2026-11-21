import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and extract Month
    df['Date'] = pd.to_datetime(df['Date'])
    df['month'] = df['Date'].dt.month
    
    # 2. Melt the hourly columns (1-24) into long format
    # Identify hour columns
    hour_cols = [str(i) for i in range(1, 25)]
    
    # Melt
    df_melted = df.melt(
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour', 
        value_name='value'
    )
    
    # Convert hour to integer for proper sorting/aggregation
    df_melted['hour'] = df_melted['hour'].astype(int)
    
    # 3. Aggregate by Month and Hour
    # Calculate mean value for each month and hour
    agg_df = df_melted.groupby(['month', 'hour'])['value'].mean().reset_index()
    
    # 4. Pivot to wide format: Index=hour, Columns=month
    pivot_df = agg_df.pivot(index='hour', columns='month', values='value')
    
    # 5. Rename month columns to lowercase names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivot_df = pivot_df.rename(columns=month_map)
    
    # 6. Ensure all month columns exist, even if empty (NaN)
    target_months = [
        'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Reindex columns to ensure order and presence
    pivot_df = pivot_df.reindex(columns=target_months)
    
    # 7. Reset index to make 'hour' a column
    result_df = pivot_df.reset_index()
    
    # 8. Sort by hour to ensure deterministic order (1-24)
    result_df = result_df.sort_values('hour').reset_index(drop=True)
    
    # 9. Define final target columns
    target_columns = ['hour'] + target_months
    
    return result_df[target_columns]