import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and extract Month
    df['Date'] = pd.to_datetime(df['Date'])
    df['month'] = df['Date'].dt.month
    
    # 2. Melt the hourly columns to long format
    # Identify hour columns
    hour_cols = [f'Hr {i}' for i in range(1, 25)]
    
    # Melt: id_vars keep Date and month, value_vars are the hour columns
    melted = df.melt(
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_str', 
        value_name='value'
    )
    
    # 3. Parse hour number from 'Hr 1' -> 1
    melted['hour'] = melted['hour_str'].str.replace('Hr ', '', regex=False).astype(int)
    
    # 4. Group by hour and month, calculate mean
    # The target seems to be the average value for each hour across all days in that month
    grouped = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 5. Pivot to get months as columns
    # Index: hour, Columns: month, Values: value
    pivoted = grouped.pivot(index='hour', columns='month', values='value')
    
    # 6. Rename month columns to lowercase names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivoted.columns = [month_map[col] for col in pivoted.columns]
    
    # 7. Reset index to make 'hour' a column
    df_result = pivoted.reset_index()
    
    # 8. Ensure correct column order and types
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # Sort by hour just in case
    df_result = df_result.sort_values('hour').reset_index(drop=True)
    
    # Ensure hour is int64
    df_result['hour'] = df_result['hour'].astype(int)
    
    return df_result[target_columns]