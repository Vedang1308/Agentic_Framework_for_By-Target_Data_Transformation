import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract Hour and Month
    df['Hour'] = df['dt'].dt.hour
    df['MonthNum'] = df['dt'].dt.month
    
    # 3. Map Month Numbers to Names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['MonthName'] = df['MonthNum'].map(month_map)
    
    # 4. Pivot the data
    # Aggregate using mean. If values are constant per hour/month, mean == value.
    # If multiple values exist, mean provides a summary.
    pivot_df = df.pivot_table(
        index='Hour', 
        columns='MonthName', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 5. Ensure all hours 0-23 are present
    all_hours = pd.RangeIndex(0, 24, name='Hour')
    pivot_df = pivot_df.reindex(all_hours)
    
    # 6. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Define target columns
    target_columns = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
    
    # 8. Select and order columns
    # Note: pivot_df columns might not be in order, so we select explicitly
    result_df = pivot_df[target_columns]
    
    # Ensure Hour is int64
    result_df['Hour'] = result_df['Hour'].astype('int64')
    
    return result_df