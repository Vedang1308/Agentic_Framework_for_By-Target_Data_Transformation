import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Aggregate by date and hour
    # We use mean to handle multiple entries per hour. 
    # If there are no entries for a specific hour on a day, it will be NaN.
    agg_df = df.groupby(['date_only', 'hour'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 4. Pivot the table
    # Index: date_only, Columns: hour, Values: zone_016_cooling_sp
    pivot_df = agg_df.pivot(index='date_only', columns='hour', values='zone_016_cooling_sp')
    
    # 5. Ensure all 24 hours are present as columns
    # The pivot might only have columns for hours that had data.
    # We need columns 0 through 23.
    all_hours = range(24)
    pivot_df = pivot_df.reindex(columns=all_hours)
    
    # 6. Rename columns to "Hr 1", "Hr 2", ..., "Hr 24"
    # Hour 0 -> Hr 1, Hour 1 -> Hr 2, ..., Hour 23 -> Hr 24
    pivot_df.columns = [f'Hr {h+1}' for h in pivot_df.columns]
    
    # 7. Format the date index to string '%m/%d/%Y'
    pivot_df.index = pivot_df.index.strftime('%m/%d/%Y')
    
    # 8. Reset index to make 'Date' a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_only': 'Date'})
    
    # 9. Define target columns
    target_columns = ['Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24']
    
    # 10. Ensure the order and presence of columns
    # Reindex to ensure all target columns are present and in order
    pivot_df = pivot_df.reindex(columns=target_columns)
    
    return pivot_df[target_columns]