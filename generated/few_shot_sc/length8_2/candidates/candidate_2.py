import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract Hour and Month
    df['Hour'] = df['datetime'].dt.hour
    df['Month_Num'] = df['datetime'].dt.month
    
    # 3. Map Month numbers to names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['Month_Name'] = df['Month_Num'].map(month_names)
    
    # 4. Aggregate and Pivot
    # Group by Hour and Month_Name, calculate mean of zone_016
    pivot_df = df.pivot_table(
        index='Hour', 
        columns='Month_Name', 
        values='zone_016', 
        aggfunc='mean'
    )
    
    # 5. Reset index and clean up
    pivot_df = pivot_df.reset_index()
    
    # Ensure Hour is integer type
    pivot_df['Hour'] = pivot_df['Hour'].astype(int)
    
    # Define target columns
    target_columns = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
    
    # Ensure all month columns exist (fill missing with NaN if necessary, though pivot_table usually handles this)
    for col in target_columns[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # Sort by Hour
    pivot_df = pivot_df.sort_values('Hour').reset_index(drop=True)
    
    # Select and return target columns
    return pivot_df[target_columns]