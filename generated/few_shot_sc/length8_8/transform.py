import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse date and extract month
    df['date_dt'] = pd.to_datetime(df['date'])
    df['month_num'] = df['date_dt'].dt.month
    
    # Map month numbers to lowercase names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df['month_name'] = df['month_num'].map(month_map)
    
    # 2. Melt the hourly columns
    # Identify hourly columns
    hour_cols = [f'Hour {i}' for i in range(1, 25)]
    
    # Melt
    df_melted = df.melt(
        id_vars=['month_name'],
        value_vars=hour_cols,
        var_name='hour_col',
        value_name='value'
    )
    
    # Extract hour number from 'Hour 1' -> 1
    df_melted['hour'] = df_melted['hour_col'].str.extract(r'(\d+)').astype(int)
    
    # 3. Aggregate
    # Group by month and hour, calculate mean
    # Using mean to handle multiple days in the same month/hour
    agg_df = df_melted.groupby(['month_name', 'hour'])['value'].mean().reset_index()
    
    # 4. Pivot to wide format
    # Rows: hour, Columns: month_name, Values: value
    pivot_df = agg_df.pivot(index='hour', columns='month_name', values='value')
    
    # 5. Ensure all months are present in columns, even if NaN
    all_months = [month_map[i] for i in range(1, 13)]
    pivot_df = pivot_df.reindex(columns=all_months)
    
    # 6. Reset index and rename
    pivot_df = pivot_df.reset_index()
    pivot_df.columns.name = None # Clear column name
    
    # 7. Sort by hour
    pivot_df = pivot_df.sort_values('hour').reset_index(drop=True)
    
    # 8. Select target columns verbatim
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    return pivot_df[target_columns]