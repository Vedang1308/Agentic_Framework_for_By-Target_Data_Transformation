import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['date_parsed'].dt.hour
    df['Month_Num'] = df['date_parsed'].dt.month
    
    # 3. Map Month Number to Month Name
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['Month_Name'] = df['Month_Num'].map(month_map)
    
    # 4. Pivot the table
    # Index: Hour, Columns: Month_Name, Values: zone_016_cooling_sp
    # Using mean to aggregate potential duplicates for the same hour/month
    pivot_df = df.pivot_table(
        index='Hour', 
        columns='Month_Name', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 5. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Define target columns
    target_columns = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
    
    # 7. Ensure all month columns exist, even if empty
    for month in target_columns[1:]:
        if month not in pivot_df.columns:
            pivot_df[month] = np.nan
            
    # 8. Sort by Hour to match target order
    pivot_df = pivot_df.sort_values('Hour').reset_index(drop=True)
    
    # 9. Ensure Hour is integer type
    pivot_df['Hour'] = pivot_df['Hour'].astype('int64')
    
    # 10. Select and return only the target columns in the correct order
    return pivot_df[target_columns]