import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['date_dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month Name
    df['Hour'] = df['date_dt'].dt.hour
    df['Month'] = df['date_dt'].dt.strftime('%B') # Full month name e.g., 'January'
    
    # 3. Pivot the data
    # Index: Hour, Columns: Month, Values: zone_016_cooling_sp
    # Aggregation: mean (standard for binning time-series data)
    pivot_df = df.pivot_table(
        index='Hour', 
        columns='Month', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 4. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 5. Define target column order
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    target_columns = ['Hour'] + month_names
    
    # 6. Ensure all month columns exist (even if empty/NaN) and are in correct order
    # pivot_table might miss months if no data exists for them, but reset_index keeps existing ones.
    # We need to make sure we return exactly the target columns.
    
    # Re-index columns to ensure order and presence
    # If a month is missing from pivot_df, it will be NaN in the final selection if we just select.
    # But pivot_df columns are the months that had data. We need to ensure all 12 months are present as columns.
    
    # Create a complete frame with all months
    for month in month_names:
        if month not in pivot_df.columns:
            pivot_df[month] = np.nan
            
    # Sort by Hour to match typical target output order (0-23)
    pivot_df = pivot_df.sort_values('Hour').reset_index(drop=True)
    
    # Select final columns
    return pivot_df[target_columns]