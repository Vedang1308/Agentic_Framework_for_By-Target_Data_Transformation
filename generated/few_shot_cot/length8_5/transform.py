import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse date and extract month
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    df['month_num'] = df['date_parsed'].dt.month
    
    # Map month numbers to lowercase names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df['month_name'] = df['month_num'].map(month_map)
    
    # 2. Melt the value columns (value1...value24) into long format
    # Identify value columns
    value_cols = [f'value{i}' for i in range(1, 25)]
    
    melted = df.melt(
        id_vars=['month_name'], 
        value_vars=value_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # Extract hour integer from column name (e.g., 'value1' -> 1)
    melted['hour'] = melted['hour_col'].str.extract(r'(\d+)').astype(int)
    
    # 3. Aggregate by hour and month
    # Calculate mean value for each hour and month combination
    aggregated = melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 4. Pivot to wide format
    # Index: hour, Columns: month_name, Values: value
    pivoted = aggregated.pivot(index='hour', columns='month_name', values='value')
    
    # Reset index to make 'hour' a column
    pivoted = pivoted.reset_index()
    
    # Ensure hour is integer
    pivoted['hour'] = pivoted['hour'].astype(int)
    
    # 5. Define target columns and select
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Ensure all target month columns exist (fill NaN if a month is missing in data)
    for col in target_columns[1:]:
        if col not in pivoted.columns:
            pivoted[col] = np.nan
            
    # Sort by hour to ensure consistent ordering (1-24)
    pivoted = pivoted.sort_values('hour').reset_index(drop=True)
    
    return pivoted[target_columns]