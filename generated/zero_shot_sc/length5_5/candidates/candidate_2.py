import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with 5-minute interval cooling setpoint data
    into a daily summary DataFrame with 24 hourly columns (value1 to value24).
    """
    # 1. Parse the date column
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date (day) and hour for grouping
    df['date_only'] = df['date'].dt.normalize() # Floor to midnight
    df['hour'] = df['date'].dt.hour # 0-23
    
    # 3. Group by date and hour, and aggregate the cooling setpoint
    # Using mean as the aggregation function. Since values are likely constant within an hour 
    # or discrete setpoints, mean is a robust representative.
    # If there are multiple entries per hour, mean averages them.
    # If there is one entry, it returns that value.
    grouped = df.groupby(['date_only', 'hour'])['zone_016_cooling_sp'].mean()
    
    # 4. Unstack the hour to create columns
    # This creates a DataFrame where index is date_only and columns are 0..23
    df_pivot = grouped.unstack(level='hour')
    
    # 5. Rename columns to value1...value24
    # Map hour 0 -> value1, hour 1 -> value2, ..., hour 23 -> value24
    new_columns = {h: f'value{h+1}' for h in range(24)}
    df_pivot.rename(columns=new_columns, inplace=True)
    
    # 6. Reset index to make date_only a column
    df_pivot.reset_index(inplace=True)
    
    # 7. Format the date column to match target format '%m/%d/%Y'
    df_pivot['date'] = df_pivot['date_only'].dt.strftime('%m/%d/%Y')
    
    # 8. Define the exact target column order
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 9. Select and return the columns in the correct order
    # Ensure all 24 value columns exist, filling with NaN if a specific hour is missing for a day
    for col in target_columns[1:]:
        if col not in df_pivot.columns:
            df_pivot[col] = np.nan
            
    return df_pivot[target_columns]