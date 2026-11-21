import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date column
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 2. Identify hourly columns
    hr_cols = [c for c in df.columns if c.startswith('Hr ')]
    
    # 3. Melt the dataframe to long format
    # id_vars keeps Date, value_vars are the hour columns
    melted = df.melt(
        id_vars=['Date'], 
        value_vars=hr_cols, 
        var_name='hour_str', 
        value_name='value'
    )
    
    # 4. Extract hour integer from 'Hr X' string
    melted['hour'] = melted['hour_str'].str.extract(r'(\d+)').astype(int)
    
    # 5. Extract month name from Date and convert to lowercase
    melted['month'] = melted['Date'].dt.month_name().str.lower()
    
    # 6. Group by hour and month, then calculate the mean
    # This aggregates all days for each month for each specific hour
    aggregated = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 7. Pivot to wide format: index=hour, columns=month, values=value
    pivoted = aggregated.pivot(index='hour', columns='month', values='value')
    
    # 8. Reset index to make 'hour' a column
    pivoted = pivoted.reset_index()
    
    # 9. Define target column names
    month_cols = [
        'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Ensure all month columns exist (fill NaN if any month is missing in data)
    for col in month_cols:
        if col not in pivoted.columns:
            pivoted[col] = float('nan')
            
    # 10. Select and order columns exactly as required
    target_columns = ['hour'] + month_cols
    
    # Sort by hour to ensure 1-24 order
    pivoted = pivoted.sort_values('hour').reset_index(drop=True)
    
    return pivoted[target_columns]