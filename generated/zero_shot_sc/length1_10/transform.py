import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Parse the 'date' column.
    2. Extract the formatted date string for 'cst'.
    3. Extract the hour from the timestamp, mapping 0 to 24.
    4. Group by 'cst' and 'hour', summing the 'zone_016_cooling_sp'.
    5. Pivot to wide format with hours as columns.
    6. Format columns as 'H:00'.
    7. Ensure all 24 hour columns exist and are ordered correctly.
    """
    
    # 1. Parse date
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Create 'cst' column with format '%a %m/%d/%Y'
    # %a is abbreviated weekday name (e.g., Sun, Mon)
    df['cst'] = df['datetime'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Extract hour and map 0 to 24
    # Pandas hour is 0-23. Target is 1-24.
    # 0 -> 24, 1 -> 1, ..., 23 -> 23
    df['hour_num'] = df['datetime'].dt.hour
    df['hour_num'] = df['hour_num'].replace(0, 24)
    
    # 4. Aggregate: Sum the values for each day and hour
    # We group by 'cst' and 'hour_num' and sum 'zone_016_cooling_sp'
    agg_df = df.groupby(['cst', 'hour_num'])['zone_016_cooling_sp'].sum().reset_index()
    
    # 5. Pivot to wide format
    # Index: 'cst', Columns: 'hour_num', Values: 'zone_016_cooling_sp'
    pivot_df = agg_df.pivot(index='cst', columns='hour_num', values='zone_016_cooling_sp')
    
    # 6. Fill missing hours with 0 (if a specific hour had no records, sum is 0)
    pivot_df = pivot_df.fillna(0)
    
    # 7. Reset index to make 'cst' a column
    pivot_df = pivot_df.reset_index()
    
    # 8. Rename columns to match target format 'H:00'
    # The columns are currently integers (1-24) or 'cst'
    # We need to map integer columns to strings like '1:00', '2:00', ... '24:00'
    col_mapping = {h: f"{h}:00" for h in range(1, 25)}
    pivot_df.rename(columns=col_mapping, inplace=True)
    
    # 9. Ensure all target columns exist, even if empty in this specific dataset slice
    target_columns = ['cst', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', 
                      '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', 
                      '19:00', '20:00', '21:00', '22:00', '23:00', '24:00']
    
    # Reindex columns to ensure order and presence
    # If any hour column is missing (e.g., no data for that hour), add it with 0
    for col in target_columns[1:]: # Skip 'cst'
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # Select and order columns
    result_df = pivot_df[target_columns]
    
    return result_df