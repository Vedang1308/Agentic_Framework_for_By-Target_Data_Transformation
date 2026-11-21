import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and extract month
    df['Date'] = pd.to_datetime(df['Date'])
    df['month'] = df['Date'].dt.month
    
    # 2. Identify hourly columns (1 to 24)
    hour_cols = [str(i) for i in range(1, 25)]
    
    # 3. Melt the dataframe to long format
    # id_vars keeps 'Date' and 'month', value_vars are the hours
    melted = df.melt(id_vars=['Date', 'month'], value_vars=hour_cols, var_name='hour', value_name='value')
    
    # 4. Convert hour to integer for proper sorting/grouping
    melted['hour'] = melted['hour'].astype(int)
    
    # 5. Aggregate by hour and month
    # We assume the target values are the mean of the available days for that hour/month
    aggregated = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 6. Pivot to get months as columns
    pivoted = aggregated.pivot(index='hour', columns='month', values='value')
    
    # 7. Reset index to make 'hour' a column
    pivoted = pivoted.reset_index()
    
    # 8. Rename month columns to lowercase month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivoted.rename(columns=month_names, inplace=True)
    
    # 9. Ensure 'hour' is integer type
    pivoted['hour'] = pivoted['hour'].astype(int)
    
    # 10. Sort by hour to ensure canonical order (1-24)
    pivoted = pivoted.sort_values('hour').reset_index(drop=True)
    
    # 11. Define target columns verbatim
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    return pivoted[target_columns]