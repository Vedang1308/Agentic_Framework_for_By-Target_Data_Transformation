import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['datetime'].dt.hour
    df['Month'] = df['datetime'].dt.month
    
    # 3. Define month name mapping
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    # Map month numbers to names
    df['Month_Name'] = df['Month'].map(month_names)
    
    # 4. Aggregate and Pivot
    # We group by Hour and Month_Name, then take the mean of the cooling setpoint
    # Using pivot_table to handle the reshaping and aggregation
    pivot_df = df.pivot_table(
        index='Hour', 
        columns='Month_Name', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 5. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Ensure all month columns exist and are in the correct order
    target_months = ['January', 'February', 'March', 'April', 'May', 'June', 
                     'July', 'August', 'September', 'October', 'November', 'December']
    
    # Reindex columns to ensure all months are present (filling missing with NaN)
    # The pivot table might not have all months if data is sparse
    all_cols = ['Hour'] + target_months
    pivot_df = pivot_df.reindex(columns=all_cols)
    
    # 7. Ensure Hour is integer type
    pivot_df['Hour'] = pivot_df['Hour'].astype(int)
    
    # 8. Return the final dataframe
    return pivot_df