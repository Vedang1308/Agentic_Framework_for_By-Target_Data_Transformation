import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source electricity demand data into the target format.
    
    Steps:
    1. Parse the 'Date' column.
    2. Extract 'month' name and 'daytype' (weekday/weekend).
    3. Rename hour columns from '1:00'...'24:00:00' to 'hr1'...'hr24'.
    4. Construct the final DataFrame with the correct schema.
    """
    # 1. Parse Date
    # Format is '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    dt_series = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # 2. Extract Target Features
    # Month name (e.g., 'October')
    month_names = dt_series.dt.month_name()
    
    # Day type: weekday if Mon-Fri (0-4), weekend if Sat-Sun (5-6)
    daytypes = np.where(dt_series.dt.weekday < 5, 'weekday', 'weekend')
    
    # 3. Prepare Hour Columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: hr1, hr2, ..., hr23, hr24
    
    # Create a mapping for the hour columns
    hour_mapping = {}
    for i in range(1, 24):
        hour_mapping[f'{i}:00'] = f'hr{i}'
    hour_mapping['24:00:00'] = 'hr24'
    
    # Rename the hour columns in a copy of the source to avoid SettingWithCopyWarning
    # We only need the hour columns and the new calculated columns
    df_hours = source[list(hour_mapping.keys())].copy()
    df_hours = df_hours.rename(columns=hour_mapping)
    
    # 4. Construct Final DataFrame
    df = pd.DataFrame()
    df['month'] = month_names
    df['daytype'] = daytypes
    
    # Append the hour columns in the correct order
    for i in range(1, 25):
        df[f'hr{i}'] = df_hours[f'hr{i}']
        
    # Define the exact target column order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    return df[target_columns]