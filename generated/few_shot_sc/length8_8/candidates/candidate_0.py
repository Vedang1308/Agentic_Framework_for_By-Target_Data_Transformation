import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse dates and extract month names (lowercase)
    df['date_dt'] = pd.to_datetime(df['date'])
    df['month'] = df['date_dt'].dt.month_name().str.lower()
    
    # 2. Identify hour columns
    hour_cols = [f'Hour {i}' for i in range(1, 25)]
    
    # 3. Melt the dataframe to long format
    # We keep 'month' as an identifier and melt all hour columns
    melted = df.melt(
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # 4. Extract integer hour from the 'hour_col' string (e.g., 'Hour 1' -> 1)
    melted['hour'] = melted['hour_col'].str.extract('(\d+)').astype(int)
    
    # 5. Aggregate values by hour and month
    # Using mean to average the daily values for each hour within the month
    aggregated = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 6. Pivot to wide format: rows=hour, columns=month
    pivoted = aggregated.pivot(index='hour', columns='month', values='value')
    
    # 7. Clean up column names to be lowercase (though month_name().str.lower() already did this, pivot preserves keys)
    # Ensure column names are strings and lowercase
    pivoted.columns = [str(col).lower() for col in pivoted.columns]
    
    # 8. Reset index to make 'hour' a column
    result = pivoted.reset_index()
    
    # 9. Define target columns verbatim
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # 10. Select and return the target columns
    return result[target_columns]