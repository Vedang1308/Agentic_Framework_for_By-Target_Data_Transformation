import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Parse the 'date' column into datetime.
    2. Extract 'Hour' and 'Month' from the datetime.
    3. Map Month numbers to Month names.
    4. Pivot the table to have Hours as rows and Months as columns, 
       aggregating 'zone_016' by mean.
    5. Format the output to match the target schema.
    """
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse date column
    # Format inferred: %m/%d/%Y %H:%M
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
    df['Month_Name'] = df['Month'].map(month_map)
    
    # 4. Pivot the table
    # Index: Hour
    # Columns: Month_Name
    # Values: zone_016
    # Aggregation: mean (to handle multiple days/minutes per hour/month)
    pivot_df = df.pivot_table(
        index='Hour',
        columns='Month_Name',
        values='zone_016',
        aggfunc='mean'
    )
    
    # 5. Reset index to bring Hour back as a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Define target columns
    target_columns = [
        'Hour', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # 7. Ensure all month columns exist (in case some months are missing in data)
    for col in target_columns[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 8. Select and order columns
    result_df = pivot_df[target_columns]
    
    # 9. Ensure Hour is int64
    result_df['Hour'] = result_df['Hour'].astype('int64')
    
    return result_df