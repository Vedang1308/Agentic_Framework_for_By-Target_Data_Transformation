import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month Name
    df['Hour'] = df['datetime'].dt.hour
    df['Month_Name'] = df['datetime'].dt.month_name()
    
    # 3. Define the target month columns in order
    target_months = [
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # 4. Pivot the data
    # We group by Hour and Month_Name and aggregate the cooling_sp values.
    # Using 'mean' handles potential duplicates for the same hour/month.
    pivot_df = df.pivot_table(
        index='Hour', 
        columns='Month_Name', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 5. Ensure all target month columns exist, filling missing with NaN
    pivot_df = pivot_df.reindex(columns=target_months)
    
    # 6. Sort by Hour and reset index
    pivot_df = pivot_df.sort_index()
    pivot_df = pivot_df.reset_index()
    
    # 7. Define final target columns
    target_columns = ['Hour'] + target_months
    
    # 8. Select and return
    df_result = pivot_df[target_columns]
    
    # Ensure correct types
    df_result['Hour'] = df_result['Hour'].astype('int64')
    for col in target_months:
        df_result[col] = df_result[col].astype('float64')
        
    return df_result[target_columns]