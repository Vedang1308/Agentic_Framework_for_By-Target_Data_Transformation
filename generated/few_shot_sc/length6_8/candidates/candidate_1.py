import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source DataFrame with timestamped logger data into a daily hourly summary.
    
    Steps:
    1. Parse the 'date' column to datetime.
    2. Extract the date string ('%m/%d/%Y') and the hour (1-24 mapping).
    3. Group by Date and Hour, aggregating 'cerc_logger_1' using mean.
    4. Pivot/unstack to wide format with columns 'Hr 1' to 'Hr 24'.
    5. Format and return the final DataFrame.
    """
    df = source.copy()
    
    # 1. Parse datetime
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract Date string and Hour
    # Target Date format: %m/%d/%Y
    df['Date'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # Target Hours are 1-24. 
    # Standard pandas hour is 0-23.
    # Mapping: 0 -> 1, 1 -> 2, ..., 23 -> 24.
    df['Hr_Num'] = df['dt'].dt.hour + 1
    
    # 3. Group by Date and Hour, aggregate mean of cerc_logger_1
    # Using mean as the standard aggregation for continuous sensor data unless specified otherwise.
    grouped = df.groupby(['Date', 'Hr_Num'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot to wide format
    # Index: Date, Columns: Hr_Num, Values: cerc_logger_1
    pivot_df = grouped.pivot(index='Date', columns='Hr_Num', values='cerc_logger_1')
    
    # 5. Rename columns to 'Hr 1', 'Hr 2', ..., 'Hr 24'
    pivot_df.columns = [f'Hr {int(col)}' for col in pivot_df.columns]
    
    # Reset index to make Date a column
    pivot_df = pivot_df.reset_index()
    
    # Define target columns in exact order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # Ensure all target columns exist (in case some hours are missing in data, they will be NaN)
    # The problem implies a complete target table, so we select only existing columns 
    # or fill missing if necessary. However, strict selection is safer.
    # If a column is missing from pivot_df (e.g., no data for Hr 5 on a specific day), 
    # pivot creates NaN. If the column doesn't exist in the index at all (no data for that hour globally), 
    # it won't be in columns. We should ensure all 24 columns are present.
    
    for col in target_columns[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # Return with exact column order
    return pivot_df[target_columns]