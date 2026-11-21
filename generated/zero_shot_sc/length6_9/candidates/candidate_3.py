import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Date and Hour components
    # Target 'Date' is MM/DD/YYYY
    df['Date'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    # Target 'Hr 1' corresponds to Hour 0, 'Hr 2' to Hour 1, etc.
    df['Hour'] = df['parsed_date'].dt.hour
    
    # 3. Pivot the data
    # We group by Date and Hour. Since there can be multiple entries per hour,
    # we need an aggregation function. 'first' is a safe bet for snapshot data,
    # preserving the first observed value for that hour.
    # We sort by parsed_date first to ensure 'first' is deterministic (earliest time).
    df = df.sort_values('parsed_date')
    
    # Create the pivot table
    # index: Date (string formatted)
    # columns: Hour (integer 0-23)
    # values: zone_016
    # aggfunc: 'first' takes the first non-null value in the group
    pivot_df = df.pivot_table(
        index='Date', 
        columns='Hour', 
        values='zone_016', 
        aggfunc='first'
    )
    
    # 4. Ensure all hours 0-23 are present as columns
    all_hours = range(24)
    pivot_df = pivot_df.reindex(columns=all_hours)
    
    # 5. Rename columns to match target schema ('Hr 1' to 'Hr 24')
    # Map hour 0 -> 'Hr 1', 1 -> 'Hr 2', ...
    pivot_df.columns = [f'Hr {h+1}' for h in pivot_df.columns]
    
    # 6. Reset index to make 'Date' a column
    result_df = pivot_df.reset_index()
    
    # 7. Define target columns in exact order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 8. Ensure column order and existence
    return result_df[target_columns]