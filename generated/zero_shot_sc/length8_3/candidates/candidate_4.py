import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month Name
    df['Hour'] = df['date'].dt.hour
    df['Month_Name'] = df['date'].dt.month
    
    # Map month numbers to names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['Month_Name'] = df['Month_Name'].map(month_map)
    
    # 3. Pivot the table
    # Index: Hour, Columns: Month_Name, Values: zone_016_cooling_sp
    # Use mean to aggregate if multiple rows exist for the same Hour/Month
    pivot_df = df.pivot_table(
        index='Hour', 
        columns='Month_Name', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 4. Ensure all month columns are present
    target_months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Reindex columns to include all months, filling missing ones with NaN
    pivot_df = pivot_df.reindex(columns=target_months)
    
    # 5. Reset index to make Hour a column again
    result_df = pivot_df.reset_index()
    
    # 6. Ensure Hour is integer
    result_df['Hour'] = result_df['Hour'].astype(int)
    
    # 7. Define final target columns
    target_columns = ['Hour'] + target_months
    
    # 8. Select and return in the exact order
    return result_df[target_columns]