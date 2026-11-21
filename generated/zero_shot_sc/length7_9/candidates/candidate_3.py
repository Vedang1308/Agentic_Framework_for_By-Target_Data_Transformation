import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Parse the 'Date' column to extract month name and day of week.
    2. Create 'month' column with full month name.
    3. Create 'daytype' column ('weekday' or 'weekend').
    4. Rename hourly columns from '1:00'...'24:00:00' to 'hr1'...'hr24'.
    5. Select and order columns to match target schema.
    """
    df = source.copy()
    
    # 1. Parse Date
    # Format is '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # 2. Extract Month Name
    df['month'] = df['parsed_date'].dt.strftime('%B')
    
    # 3. Extract Day Type
    # weekday: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    df['daytype'] = np.where(
        df['parsed_date'].dt.weekday < 5, 
        'weekday', 
        'weekend'
    )
    
    # 4. Rename Hourly Columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    rename_map = {}
    for i in range(1, 24):
        rename_map[f'{i}:00'] = f'hr{i}'
    rename_map['24:00:00'] = 'hr24'
    
    df = df.rename(columns=rename_map)
    
    # 5. Define Target Columns
    target_columns = [
        'month', 'daytype', 
        'hr1', 'hr2', 'hr3', 'hr4', 'hr5', 'hr6', 'hr7', 'hr8', 
        'hr9', 'hr10', 'hr11', 'hr12', 'hr13', 'hr14', 'hr15', 'hr16', 
        'hr17', 'hr18', 'hr19', 'hr20', 'hr21', 'hr22', 'hr23', 'hr24'
    ]
    
    # 6. Select and Return
    return df[target_columns]