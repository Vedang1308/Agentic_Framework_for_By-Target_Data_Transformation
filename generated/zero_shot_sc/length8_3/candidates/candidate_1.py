import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['date'].dt.hour
    df['Month'] = df['date'].dt.month
    
    # 3. Map Month numbers to Month names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['MonthName'] = df['Month'].map(month_map)
    
    # 4. Pivot the data
    # Index: Hour, Columns: MonthName, Values: zone_016_cooling_sp
    # Use mean to aggregate duplicate entries (e.g., multiple 5-min intervals in same hour/month)
    pivot_df = df.pivot_table(
        index='Hour', 
        columns='MonthName', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 5. Ensure all 24 hours (0-23) are present in the index
    # The target has 24 rows, implying a full daily cycle summary
    all_hours = range(24)
    pivot_df = pivot_df.reindex(all_hours)
    
    # 6. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Define target columns in the correct order
    target_columns = [
        'Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # 8. Ensure column names match exactly and order is correct
    # The pivot columns are already named by month names. 
    # We need to make sure all month columns exist (they will from the map/pivot logic if we don't filter)
    # However, pivot_table only creates columns for months present in the data.
    # We should add missing month columns as NaN if they aren't present, to ensure schema match.
    
    for col in target_columns[1:]: # Skip 'Hour'
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # Select and order columns
    result_df = pivot_df[target_columns]
    
    # 9. Type casting
    result_df['Hour'] = result_df['Hour'].astype(int)
    for col in target_columns[1:]:
        result_df[col] = result_df[col].astype(float)
        
    return result_df