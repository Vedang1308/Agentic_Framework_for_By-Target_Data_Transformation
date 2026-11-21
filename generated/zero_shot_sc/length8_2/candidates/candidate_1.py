import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by pivoting
    zone_016 values into a table of Hours vs Months, aggregating by mean.
    """
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['datetime'].dt.hour
    df['MonthNum'] = df['datetime'].dt.month
    
    # 3. Map Month Number to Month Name
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['MonthName'] = df['MonthNum'].map(month_names)
    
    # 4. Pivot the data
    # Group by Hour and MonthName, take the mean of zone_016
    # If a group is all NaN, mean will return NaN
    pivot_df = df.groupby(['Hour', 'MonthName'])['zone_016'].mean().unstack(fill_value=np.nan)
    
    # 5. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Define target columns to ensure correct order and presence
    target_columns = [
        'Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # 7. Reindex columns to ensure all months are present (even if empty/NaN)
    # and in the correct order.
    pivot_df = pivot_df.reindex(columns=target_columns)
    
    # 8. Ensure data types match target schema
    # Hour should be int64
    pivot_df['Hour'] = pivot_df['Hour'].astype('int64')
    
    # Month columns should be float64
    for col in target_columns[1:]:
        pivot_df[col] = pivot_df[col].astype('float64')
        
    return pivot_df