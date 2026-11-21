import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['datetime'].dt.hour
    df['MonthNum'] = df['datetime'].dt.month
    
    # 3. Map Month numbers to names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['MonthName'] = df['MonthNum'].map(month_names)
    
    # 4. Aggregate by Hour and MonthName
    # We use mean to aggregate the zone_016 values for each Hour/Month combination
    agg_df = df.groupby(['Hour', 'MonthName'])['zone_016'].mean().reset_index()
    
    # 5. Pivot the table
    # Index: Hour, Columns: MonthName, Values: zone_016
    pivot_df = agg_df.pivot(index='Hour', columns='MonthName', values='zone_016')
    
    # 6. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Ensure Hour is int64
    pivot_df['Hour'] = pivot_df['Hour'].astype('int64')
    
    # 8. Define target columns in the exact required order
    target_columns = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
    
    # 9. Reindex columns to ensure all month columns are present and in order
    # If any month is missing from the pivot (no data), it will be NaN, which is correct.
    # We need to make sure the columns exist.
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 10. Sort by Hour to ensure deterministic order 0-23
    pivot_df = pivot_df.sort_values('Hour').reset_index(drop=True)
    
    # 11. Select only the target columns
    return pivot_df[target_columns]