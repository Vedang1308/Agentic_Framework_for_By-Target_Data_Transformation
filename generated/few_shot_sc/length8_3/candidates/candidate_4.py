import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['date_parsed'].dt.hour
    df['Month'] = df['date_parsed'].dt.month
    
    # 3. Define month name mapping
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    # Map month numbers to names
    df['Month_Name'] = df['Month'].map(month_map)
    
    # 4. Pivot the data
    # Index: Hour, Columns: Month_Name, Values: zone_016_cooling_sp
    # Using mean aggregation. If multiple entries exist for same hour/month, average them.
    pivot_df = df.pivot_table(
        index='Hour',
        columns='Month_Name',
        values='zone_016_cooling_sp',
        aggfunc='mean'
    )
    
    # 5. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Ensure Hour is integer
    pivot_df['Hour'] = pivot_df['Hour'].astype(int)
    
    # 7. Define target columns in order
    target_columns = [
        'Hour', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # 8. Ensure all month columns exist (even if empty/nan)
    for col in target_columns[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 9. Select and return the target columns
    return pivot_df[target_columns]