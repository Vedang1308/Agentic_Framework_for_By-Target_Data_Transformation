import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse datetime
    df = source.copy()
    dt = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = dt.dt.hour
    df['Month'] = dt.dt.month
    
    # 3. Define month name mapping
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    # 4. Aggregate by Hour and Month
    # Using mean to handle potential multiple entries per hour/month.
    # If the data is clean setpoints, mean will just return the value.
    agg_df = df.groupby(['Hour', 'Month'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 5. Map month numbers to names
    agg_df['Month'] = agg_df['Month'].map(month_map)
    
    # 6. Pivot to wide format
    # Index: Hour, Columns: Month (names), Values: zone_016_cooling_sp
    pivot_df = agg_df.pivot(index='Hour', columns='Month', values='zone_016_cooling_sp')
    
    # 7. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 8. Ensure all month columns exist and are in correct order
    target_months = ['January', 'February', 'March', 'April', 'May', 'June', 
                     'July', 'August', 'September', 'October', 'November', 'December']
    
    # Reindex columns to ensure all months are present (filling missing with NaN)
    # First, ensure 'Hour' is the first column, then the months
    pivot_df = pivot_df.set_index('Hour')
    pivot_df = pivot_df.reindex(columns=target_months)
    pivot_df = pivot_df.reset_index()
    
    # 9. Sort by Hour to ensure 0-23 order
    pivot_df = pivot_df.sort_values('Hour').reset_index(drop=True)
    
    # 10. Define final target columns
    target_columns = ['Hour'] + target_months
    
    return pivot_df[target_columns]