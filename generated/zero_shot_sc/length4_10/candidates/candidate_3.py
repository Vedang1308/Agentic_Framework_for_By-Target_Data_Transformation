import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date string for grouping and hour for mapping
    df['date_str'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    df['hour'] = df['parsed_date'].dt.hour
    
    # 3. Define mapping from 24-hour integer to target column names
    hour_to_col = {
        0: '12:00 AM',
        1: '1:00 AM',
        2: '2:00 AM',
        3: '3:00 AM',
        4: '4:00 AM',
        5: '5:00 AM',
        6: '6:00 AM',
        7: '7:00 AM',
        8: '8:00 AM',
        9: '9:00 AM',
        10: '10:00 AM',
        11: '11:00 AM',
        12: '12:00 PM',
        13: '1:00 PM',
        14: '2:00 PM',
        15: '3:00 PM',
        16: '4:00 PM',
        17: '5:00 PM',
        18: '6:00 PM',
        19: '7:00 PM',
        20: '8:00 PM',
        21: '9:00 PM',
        22: '10:00 PM',
        23: '11:00 PM'
    }
    
    # Map hours to column names
    df['time_col'] = df['hour'].map(hour_to_col)
    
    # 4. Pivot the data
    # We group by date_str and time_col, aggregating zone_016_cooling_sp
    # Using 'mean' to handle multiple entries per hour (e.g., 5-min intervals)
    pivot_df = df.pivot_table(
        index='date_str',
        columns='time_col',
        values='zone_016_cooling_sp',
        aggfunc='mean'
    ).reset_index()
    
    # 5. Define the exact target column order
    target_columns = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # Ensure all target columns exist, filling missing ones with NaN if necessary
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # Rename index column 'date_str' to 'date'
    pivot_df = pivot_df.rename(columns={'date_str': 'date'})
    
    # 6. Select and order columns exactly as required
    final_columns = ['date'] + target_columns
    result_df = pivot_df[final_columns]
    
    return result_df[target_columns]