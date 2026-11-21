import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract Hour and Month
    df['Hour'] = df['datetime'].dt.hour
    df['Month_Num'] = df['datetime'].dt.month
    
    # 3. Map Month numbers to Month names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['Month_Name'] = df['Month_Num'].map(month_map)
    
    # 4. Aggregate by Hour and Month_Name
    # We use mean() to aggregate the zone_016 values for each Hour/Month combination.
    # This handles the reduction from many rows to one row per Hour/Month.
    agg_df = df.groupby(['Hour', 'Month_Name'])['zone_016'].mean().reset_index()
    
    # 5. Pivot the data
    # Index: Hour, Columns: Month_Name, Values: zone_016
    pivot_df = agg_df.pivot(index='Hour', columns='Month_Name', values='zone_016')
    
    # 6. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Ensure Hour is integer
    pivot_df['Hour'] = pivot_df['Hour'].astype(int)
    
    # 8. Define target columns in the correct order
    target_columns = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
    
    # 9. Select and return the target columns
    # Note: If a month is missing from the source data, it won't be in the pivot columns.
    # We should ensure all target columns exist, filling with NaN if necessary.
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = float('nan')
            
    return pivot_df[target_columns]