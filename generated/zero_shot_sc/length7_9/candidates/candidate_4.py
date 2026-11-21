import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by extracting
    month and daytype from the Date column and renaming hourly columns.
    """
    df = source.copy()
    
    # 1. Parse the Date column
    # Format is '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # 2. Derive 'month' column
    # Map month number to full month name
    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df['month'] = df['parsed_date'].dt.month.map(lambda x: month_names[x-1])
    
    # 3. Derive 'daytype' column
    # dayofweek: Monday=0, ..., Friday=4, Saturday=5, Sunday=6
    df['daytype'] = df['parsed_date'].dt.dayofweek.apply(
        lambda x: 'weekday' if x < 5 else 'weekend'
    )
    
    # 4. Rename hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    
    rename_mapping = {}
    for i in range(1, 24):
        rename_mapping[f'{i}:00'] = f'hr{i}'
    rename_mapping['24:00:00'] = 'hr24'
    
    df = df.rename(columns=rename_mapping)
    
    # 5. Select and order target columns
    target_columns = [
        'month', 'daytype', 'hr1', 'hr2', 'hr3', 'hr4', 'hr5', 'hr6', 'hr7', 'hr8', 
        'hr9', 'hr10', 'hr11', 'hr12', 'hr13', 'hr14', 'hr15', 'hr16', 'hr17', 'hr18', 
        'hr19', 'hr20', 'hr21', 'hr22', 'hr23', 'hr24'
    ]
    
    # Drop helper column
    if 'parsed_date' in df.columns:
        df = df.drop(columns=['parsed_date'])
        
    return df[target_columns]