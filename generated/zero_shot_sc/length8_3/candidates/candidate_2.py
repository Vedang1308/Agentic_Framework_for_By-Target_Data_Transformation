import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing date and cooling setpoint data
    into a pivoted table with Hours as rows and Months as columns.
    """
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['datetime'].dt.hour
    df['Month'] = df['datetime'].dt.month
    
    # 3. Map Month numbers to Month names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['MonthName'] = df['Month'].map(month_map)
    
    # 4. Pivot the data
    # We aggregate by Hour and MonthName. 
    # Using mean to handle cases where multiple days contribute to the same Hour/Month bin.
    pivot_df = df.pivot_table(
        index='Hour', 
        columns='MonthName', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 5. Reindex to ensure all Hours (0-23) and all Months are present
    all_hours = pd.RangeIndex(start=0, stop=24, step=1)
    all_months = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
    
    pivot_df = pivot_df.reindex(index=all_hours, columns=all_months)
    
    # 6. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'index': 'Hour'})
    
    # 7. Ensure correct column order and types
    target_columns = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
    
    # Sort by Hour just in case reindex didn't maintain order (though it should)
    pivot_df = pivot_df.sort_values('Hour').reset_index(drop=True)
    
    # Select only the target columns to ensure exact match
    result_df = pivot_df[target_columns]
    
    # Ensure Hour is int64
    result_df['Hour'] = result_df['Hour'].astype('int64')
    
    return result_df[target_columns]