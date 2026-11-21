import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    
    Steps:
    1. Parse the 'date' column.
    2. Extract the date string and hour.
    3. Map clock hours to target column names ('Hr 1' to 'Hr 24'), 
       where Clock Hour 0 maps to 'Hr 24' and others map to 'Hr {Hour}'.
    4. Aggregate data by Date and Mapped Hour.
    5. Pivot to wide format.
    6. Ensure all target columns are present.
    """
    
    # 1. Parse date and extract components
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Date string and Hour
    df['Date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    df['Hour'] = df['datetime'].dt.hour
    
    # 3. Map Hour to Target Column Name
    # Clock Hour 0 -> 'Hr 24'
    # Clock Hour 1 -> 'Hr 1'
    # ...
    # Clock Hour 23 -> 'Hr 23'
    def map_hour_to_col_name(hour):
        if hour == 0:
            return 'Hr 24'
        else:
            return f'Hr {hour}'
            
    df['Hour_Col'] = df['Hour'].apply(map_hour_to_col_name)
    
    # 4. Aggregate by Date and Hour_Col
    # Using mean to handle multiple 5-min intervals per hour
    agg_df = df.groupby(['Date', 'Hour_Col'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 5. Pivot to wide format
    pivot_df = agg_df.pivot(index='Date', columns='Hour_Col', values='zone_016_cooling_sp')
    
    # 6. Define target columns and ensure they all exist
    target_hour_cols = [f'Hr {i}' for i in range(1, 25)]
    
    # Reindex columns to ensure all Hr 1..24 are present, filling missing with NaN
    pivot_df = pivot_df.reindex(columns=target_hour_cols)
    
    # Reset index to make Date a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Construct final column list
    target_columns = ['Date'] + target_hour_cols
    
    # Ensure the final output has exactly these columns
    df_final = pivot_df[target_columns]
    
    # Optional: Ensure types are float for the hour columns (they might be object if mixed)
    for col in target_hour_cols:
        df_final[col] = pd.to_numeric(df_final[col], errors='coerce')
        
    return df_final