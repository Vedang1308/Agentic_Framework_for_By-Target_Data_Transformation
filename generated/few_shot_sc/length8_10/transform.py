import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the Date column to extract month
    # The format is '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    # We can parse it directly. Note: pd.to_datetime might struggle with the leading day name if not specified,
    # but splitting is safer or using a custom parser.
    # Let's try parsing the date part specifically.
    # Split by space, take the last part which is MM/DD/YYYY
    date_str = df['Date'].str.split(' ').str[-1]
    dt = pd.to_datetime(date_str, format='%m/%d/%Y')
    df['month'] = dt.dt.month
    
    # 2. Identify hourly columns
    # Columns are '1:00' to '24:00:00'
    # We need to melt these columns
    hourly_cols = [c for c in df.columns if c not in ['Segment', 'Date']]
    
    # 3. Melt the dataframe
    melted = df.melt(
        id_vars=['month'], 
        value_vars=hourly_cols, 
        var_name='hour_str', 
        value_name='value'
    )
    
    # 4. Extract integer hour from hour_str
    # Examples: '1:00' -> 1, '24:00:00' -> 24
    def extract_hour(h_str):
        # Split by ':' and take the first part
        return int(h_str.split(':')[0])
    
    melted['hour'] = melted['hour_str'].apply(extract_hour)
    
    # 5. Group by month and hour, and calculate mean
    aggregated = melted.groupby(['month', 'hour'])['value'].mean()
    
    # 6. Pivot to get hours as rows and months as columns
    # Reset index to make month and hour columns
    agg_df = aggregated.reset_index()
    
    # Pivot: index=hour, columns=month, values=value
    pivoted = agg_df.pivot(index='hour', columns='month', values='value')
    
    # Sort by hour
    pivoted = pivoted.sort_index()
    
    # 7. Rename month columns to lowercase month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivoted = pivoted.rename(columns=month_names)
    
    # Reset index to make 'hour' a column
    pivoted = pivoted.reset_index()
    
    # Ensure hour is integer
    pivoted['hour'] = pivoted['hour'].astype(int)
    
    # 8. Define target columns in correct order
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # Reorder columns
    result = pivoted[target_columns]
    
    return result