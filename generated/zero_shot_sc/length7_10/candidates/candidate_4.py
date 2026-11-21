import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by:
    1. Parsing the date column.
    2. Extracting month name, day type (weekday/weekend), and hour.
    3. Grouping by month, day type, and hour, then averaging the sensor values.
    4. Pivoting the data so each hour becomes a column (hr1-hr24).
    5. Formatting the output to match the target schema.
    """
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract features
    # Month name (e.g., 'August', 'April')
    df['month'] = df['datetime'].dt.strftime('%B')
    
    # Day type: weekday (Mon-Fri) or weekend (Sat-Sun)
    # dayofweek: 0=Mon, ..., 4=Fri, 5=Sat, 6=Sun
    df['daytype'] = np.where(df['datetime'].dt.dayofweek < 5, 'weekday', 'weekend')
    
    # Hour for pivoting
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Group and Aggregate
    # Group by month, daytype, and hour, then take the mean of cerc_logger_1
    grouped = df.groupby(['month', 'daytype', 'hour'])['cerc_logger_1'].mean()
    
    # 4. Pivot/Unstack
    # Unstack the hour level to create columns for each hour
    pivoted = grouped.unstack('hour')
    
    # Reset index to make month and daytype columns again
    pivoted = pivoted.reset_index()
    
    # 5. Rename columns
    # The hour columns are currently integers 0-23. We need hr1-hr24.
    # Create a mapping dictionary
    hour_col_mapping = {h: f'hr{h+1}' for h in range(24)}
    pivoted.rename(columns=hour_col_mapping, inplace=True)
    
    # 6. Define target columns
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # Ensure all hour columns exist (in case some hours are missing for a group)
    for col in target_columns[2:]:
        if col not in pivoted.columns:
            pivoted[col] = np.nan
            
    # 7. Select and order columns
    result = pivoted[target_columns]
    
    return result