import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    
    Steps:
    1. Parse the 'Date' column to extract month name and day type.
    2. Map source hourly columns ('1:00'...'24:00:00') to target hourly columns ('hr1'...'hr24').
    3. Construct the final DataFrame with columns ['month', 'daytype', 'hr1', ..., 'hr24'].
    """
    # Define target column names
    target_columns = ['month', 'daytype', 'hr1', 'hr2', 'hr3', 'hr4', 'hr5', 'hr6', 'hr7', 'hr8', 'hr9', 'hr10', 
                      'hr11', 'hr12', 'hr13', 'hr14', 'hr15', 'hr16', 'hr17', 'hr18', 'hr19', 'hr20', 'hr21', 
                      'hr22', 'hr23', 'hr24']
    
    # 1. Parse the Date column
    # Format: 'Thu 10/01/2009' -> '%a %m/%d/%Y'
    dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    
    # 2. Extract Month Name
    month = dates.dt.month_name()
    
    # 3. Extract Day Type
    # dayofweek: 0=Monday, ..., 4=Friday, 5=Saturday, 6=Sunday
    # weekday: 0-4, weekend: 5-6
    daytype = dates.dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # 4. Rename Hourly Columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    
    # Create a mapping from source column names to target column names
    # We know there are 24 hours.
    # Source columns for hours 1-23 are like '1:00', '2:00'
    # Source column for hour 24 is '24:00:00'
    
    # Let's identify the source hourly columns dynamically or explicitly
    # The source schema lists them explicitly. Let's build a list of source hourly cols
    # based on the pattern observed.
    
    # Explicitly mapping based on the known structure from the problem description
    source_hour_cols = []
    for i in range(1, 24):
        source_hour_cols.append(f'{i}:00')
    source_hour_cols.append('24:00:00')
    
    target_hour_cols = [f'hr{i}' for i in range(1, 25)]
    
    # Create a rename dictionary
    rename_map = dict(zip(source_hour_cols, target_hour_cols))
    
    # Select only the relevant columns from source to avoid issues with 'Segment' or 'Date'
    # We will construct the new df from scratch to be safe
    
    df = pd.DataFrame()
    df['month'] = month
    df['daytype'] = daytype
    
    # Add the hourly columns with renamed headers
    for src_col, tgt_col in zip(source_hour_cols, target_hour_cols):
        df[tgt_col] = source[src_col]
        
    # Ensure the column order matches the target exactly
    df = df[target_columns]
    
    return df[target_columns]