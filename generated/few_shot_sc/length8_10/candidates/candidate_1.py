import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and Extract Month
    # The Date format is '%a %m/%d/%Y', e.g., 'Thu 10/01/2009'
    # We only need the month part for grouping.
    # Split by space to get the date string part
    date_str = df['Date'].str.split(' ').str[-1]
    dt = pd.to_datetime(date_str, format='%m/%d/%Y')
    
    # Map month number to lowercase month name
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df['month_name'] = dt.dt.month.map(month_names)
    
    # 2. Melt the DataFrame to long format
    # Identify hour columns. They are '1:00' to '24:00:00'
    # All columns except 'Segment', 'Date', 'month_name' are hour columns
    id_cols = ['Segment', 'Date', 'month_name']
    hour_cols = [c for c in df.columns if c not in id_cols]
    
    melted = df.melt(
        id_vars=id_cols, 
        value_vars=hour_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # 3. Extract Hour Integer from Column Name
    # '1:00' -> 1, '24:00:00' -> 24
    def extract_hour(col_name):
        # Split by ':' and take the first part
        return int(str(col_name).split(':')[0])
    
    melted['hour'] = melted['hour_col'].apply(extract_hour)
    
    # 4. Aggregate: Mean value for each hour and month
    # Group by hour and month_name, then calculate mean
    aggregated = melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 5. Pivot to wide format
    # Index: hour, Columns: month_name, Values: value
    pivoted = aggregated.pivot(index='hour', columns='month_name', values='value')
    
    # Reset index to make 'hour' a column
    result = pivoted.reset_index()
    
    # Rename 'hour' to 'hour' (already is, but ensure type)
    result.rename(columns={'hour': 'hour'}, inplace=True)
    
    # Ensure month columns are lowercase (they should be from mapping)
    # Fill NaNs if any month/hour combination is missing (though unlikely with full data)
    result = result.fillna(0)
    
    # Define target columns
    target_columns = ['hour'] + [
        'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Select and reorder columns
    # Note: The pivot might not have all months if data is sparse, but we assume complete data.
    # We explicitly select these columns.
    
    # Sort by hour to ensure deterministic order (1 to 24)
    result = result.sort_values(by='hour').reset_index(drop=True)
    
    return result[target_columns]