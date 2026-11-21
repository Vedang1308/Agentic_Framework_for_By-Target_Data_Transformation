import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse dates and extract month
    df['date_dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    df['month'] = df['date_dt'].dt.month
    
    # 2. Melt the hourly value columns
    # Identify value columns
    value_cols = [c for c in df.columns if c.startswith('value')]
    
    # Melt: id_vars are date and month, value_vars are the hourly columns
    melted = df.melt(
        id_vars=['date_dt', 'month'], 
        value_vars=value_cols, 
        var_name='hour_str', 
        value_name='val'
    )
    
    # 3. Convert hour_str ('value1', 'value2'...) to integer hour (1, 2...)
    melted['hour'] = melted['hour_str'].str.replace('value', '', regex=False).astype(int)
    
    # 4. Group by hour and month, and calculate the mean
    # This aggregates all days in a specific month for each specific hour
    grouped = melted.groupby(['hour', 'month'])['val'].mean().reset_index()
    
    # 5. Pivot to wide format: index=hour, columns=month, values=val
    pivoted = grouped.pivot(index='hour', columns='month', values='val')
    
    # 6. Map month numbers to month names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivoted = pivoted.rename(columns=month_map)
    
    # 7. Reset index to make 'hour' a column again
    pivoted = pivoted.reset_index()
    
    # 8. Define target columns in the exact required order
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # Ensure all target columns exist (fill with NaN if a month is missing)
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = float('nan')
            
    # Select and return only the target columns
    # Note: The sample target is not sorted by hour, but standard practice is to return sorted or 
    # whatever the pivot produces. The pivot produces sorted index (1..24). 
    # If strict row order matching the sample is required, we would need to know the specific order.
    # However, usually "contents" implies the data values. I will sort by hour for determinism.
    pivoted = pivoted.sort_values('hour').reset_index(drop=True)
    
    return pivoted[target_columns]