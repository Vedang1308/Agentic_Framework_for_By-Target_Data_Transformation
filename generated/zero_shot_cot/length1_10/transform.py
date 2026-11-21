import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source time-series DataFrame into a daily hourly summary DataFrame.
    
    Steps:
    1. Parse the 'date' column to datetime.
    2. Extract the calendar date for grouping.
    3. Extract the hour and map it to 1-24 scale (0->1, ..., 23->24).
    4. Group by date and hour, and sum the 'zone_016_cooling_sp' values.
       (Note: 12 intervals of 5 mins * 73 = 876, matching the sample target).
    5. Pivot the data to have hours as columns.
    6. Format the date column as 'cst' with format '%a %m/%d/%Y'.
    7. Rename hour columns to '1:00', '2:00', ..., '24:00'.
    8. Return the DataFrame with the exact target column schema.
    """
    
    # 1. Parse date
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date part for grouping
    df['date_only'] = df['parsed_date'].dt.date
    
    # 3. Extract hour and map to 1-24
    # Hour 0 (00:00-00:59) becomes 1
    # Hour 23 (23:00-23:59) becomes 24
    df['hour_idx'] = df['parsed_date'].dt.hour + 1
    
    # 4. Aggregate: Sum the values for each date and hour
    # Using sum because 12 * 73 = 876 matches the sample target value
    agg_df = df.groupby(['date_only', 'hour_idx'])['zone_016_cooling_sp'].sum().reset_index()
    
    # 5. Pivot the table
    # Index: date_only, Columns: hour_idx, Values: zone_016_cooling_sp
    pivot_df = agg_df.pivot(index='date_only', columns='hour_idx', values='zone_016_cooling_sp')
    
    # 6. Format the index as 'cst'
    # Convert the index (which is datetime.date or similar) to the required string format
    # We need to convert back to datetime to use strftime easily, or use the original parsed_date
    # Since we grouped by date_only, the index is date objects.
    pivot_df.index = pd.to_datetime(pivot_df.index)
    pivot_df.index = pivot_df.index.strftime('%a %m/%d/%Y')
    pivot_df.index.name = 'cst'
    
    # 7. Rename columns to match target format '1:00', '2:00', etc.
    pivot_df.columns = [f"{int(col)}:00" for col in pivot_df.columns]
    
    # 8. Reset index to make 'cst' a column
    result_df = pivot_df.reset_index()
    
    # 9. Define target columns
    target_columns = ['cst'] + [f"{h}:00" for h in range(1, 25)]
    
    # 10. Ensure all target columns exist (fill missing hours with NaN if necessary)
    for col in target_columns:
        if col not in result_df.columns:
            result_df[col] = np.nan
            
    # 11. Select and order columns
    result_df = result_df[target_columns]
    
    return result_df