import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source daily hourly data into a monthly hourly average table.
    """
    # 1. Parse the Date column to extract month information
    # Format: 'Thu 10/01/2009' -> '%a %m/%d/%Y'
    source['parsed_date'] = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    source['month'] = source['parsed_date'].dt.month
    
    # 2. Identify hour columns and melt the dataframe
    # Columns are like '1:00', '2:00', ..., '24:00:00'
    hour_cols = [c for c in source.columns if c not in ['Segment', 'Date', 'parsed_date', 'month']]
    
    # Create a mapping from column name to hour integer
    # e.g., '1:00' -> 1, '24:00:00' -> 24
    hour_mapping = {}
    for col in hour_cols:
        # Split by ':' and take the first part, convert to int
        hour_val = int(col.split(':')[0])
        hour_mapping[col] = hour_val
        
    # Melt the dataframe
    # id_vars: keep Segment, Date, parsed_date, month
    # value_vars: the hour columns
    # var_name: will hold the original column name, which we map to hour
    # value_name: the measurement value
    melted = source.melt(
        id_vars=['Segment', 'Date', 'parsed_date', 'month'],
        value_vars=hour_cols,
        var_name='hour_col',
        value_name='value'
    )
    
    # Map the hour_col to integer hour
    melted['hour'] = melted['hour_col'].map(hour_mapping)
    
    # 3. Aggregate by hour and month
    # We want the mean value for each hour in each month
    # Group by 'hour' and 'month', take mean of 'value'
    agg_df = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 4. Pivot the table
    # Index: hour, Columns: month, Values: value
    pivot_df = agg_df.pivot(index='hour', columns='month', values='value')
    
    # 5. Clean up and rename
    # Reset index to make 'hour' a column
    pivot_df = pivot_df.reset_index()
    
    # Define month names mapping
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    # Rename month columns
    pivot_df.rename(columns=month_names, inplace=True)
    
    # Ensure hour is integer
    pivot_df['hour'] = pivot_df['hour'].astype(int)
    
    # 6. Define target columns in the correct order
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Sort by hour to ensure deterministic output (standard practice)
    pivot_df = pivot_df.sort_values(by='hour').reset_index(drop=True)
    
    # Return only the target columns
    return pivot_df[target_columns]