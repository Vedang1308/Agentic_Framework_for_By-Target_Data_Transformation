import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame to the target schema by parsing dates,
    deriving month and day type, and renaming hourly columns.
    """
    df = source.copy()
    
    # 1. Parse the CST column to datetime
    # Format is '%a %m/%d/%Y' e.g., 'Sat 12/01/2012'
    df['parsed_date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    
    # 2. Derive 'month' column
    # Extract full month name (e.g., 'April', 'November')
    df['month'] = df['parsed_date'].dt.month_name()
    
    # 3. Derive 'daytype' column
    # dayofweek: Monday=0, ..., Friday=4, Saturday=5, Sunday=6
    # Weekday if dayofweek < 5, else Weekend
    df['daytype'] = np.where(df['parsed_date'].dt.dayofweek < 5, 'weekday', 'weekend')
    
    # 4. Rename hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'hr{i}'
    rename_dict['24:00:00'] = 'hr24'
    
    df = df.rename(columns=rename_dict)
    
    # 5. Define target columns verbatim
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Select and return only the required columns
    return df[target_columns]