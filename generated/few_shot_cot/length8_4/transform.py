import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column to extract month
    df['DT_STRATA'] = pd.to_datetime(df['DT_STRATA'])
    df['month_num'] = df['DT_STRATA'].dt.month
    
    # Map month numbers to lowercase month names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df['month_name'] = df['month_num'].map(month_map)
    
    # 2. Identify hourly columns
    # Columns are PCT_HOURLY_0100 to PCT_HOURLY_2400
    hourly_cols = [c for c in df.columns if c.startswith('PCT_HOURLY_') and c != 'PCT_HOURLY_2500']
    
    # 3. Melt the dataframe to long format
    # We keep 'month_name' and melt the hourly columns
    # id_vars should include the grouping key 'month_name'
    # We need to extract the hour from the column name
    
    # Create a mapping from column name to hour integer
    col_to_hour = {}
    for col in hourly_cols:
        # Extract the number part, e.g., '0100' -> 1
        # The format is PCT_HOURLY_HHMM
        hhmm = col.split('_')[-1]
        hour = int(hhmm[:2])
        col_to_hour[col] = hour
        
    # Melt
    melted = df.melt(
        id_vars=['month_name'], 
        value_vars=hourly_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # Add hour integer column
    melted['hour'] = melted['hour_col'].map(col_to_hour)
    
    # 4. Group by hour and month_name, and calculate the mean
    # Note: We assume we want the average percentage for that hour across all days in that month
    agg_df = melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 5. Pivot to get months as columns and hours as rows
    pivot_df = agg_df.pivot(index='hour', columns='month_name', values='value')
    
    # 6. Clean up and format
    pivot_df = pivot_df.reset_index()
    
    # Ensure all month columns are present and in correct order
    target_months = ['january', 'february', 'march', 'april', 'may', 'june', 
                     'july', 'august', 'september', 'october', 'november', 'december']
    
    # Reindex columns to ensure order and presence (filling NaN if a month is missing for an hour)
    # Although with full data, all should be present.
    pivot_df = pivot_df.reindex(columns=['hour'] + target_months)
    
    # Ensure hour is integer type
    pivot_df['hour'] = pivot_df['hour'].astype(int)
    
    # Sort by hour
    pivot_df = pivot_df.sort_values('hour').reset_index(drop=True)
    
    # Define target columns verbatim
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    return pivot_df[target_columns]