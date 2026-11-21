import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Extract 'month' as full name (e.g., 'January')
    df['month'] = df['date_parsed'].dt.strftime('%B')
    
    # 3. Extract 'daytype'
    # dayofweek: 0=Monday, ..., 4=Friday, 5=Saturday, 6=Sunday
    df['daytype'] = np.where(df['date_parsed'].dt.dayofweek < 5, 'weekday', 'weekend')
    
    # 4. Define mapping for hourly columns to hr1-hr24
    # Source columns are strings like "1:00 AM", "12:00 PM", etc.
    # Mapping:
    # 1:00 AM -> hr1
    # 2:00 AM -> hr2
    # ...
    # 11:00 AM -> hr11
    # 12:00 PM -> hr12
    # 1:00 PM -> hr13
    # ...
    # 11:00 PM -> hr23
    # 12:00 AM -> hr24
    
    hour_mapping = {
        '1:00 AM': 'hr1',
        '2:00 AM': 'hr2',
        '3:00 AM': 'hr3',
        '4:00 AM': 'hr4',
        '5:00 AM': 'hr5',
        '6:00 AM': 'hr6',
        '7:00 AM': 'hr7',
        '8:00 AM': 'hr8',
        '9:00 AM': 'hr9',
        '10:00 AM': 'hr10',
        '11:00 AM': 'hr11',
        '12:00 PM': 'hr12',
        '1:00 PM': 'hr13',
        '2:00 PM': 'hr14',
        '3:00 PM': 'hr15',
        '4:00 PM': 'hr16',
        '5:00 PM': 'hr17',
        '6:00 PM': 'hr18',
        '7:00 PM': 'hr19',
        '8:00 PM': 'hr20',
        '9:00 PM': 'hr21',
        '10:00 PM': 'hr22',
        '11:00 PM': 'hr23',
        '12:00 AM': 'hr24'
    }
    
    # 5. Rename the hourly columns
    df = df.rename(columns=hour_mapping)
    
    # 6. Define target columns in the correct order
    target_columns = ['month', 'daytype', 'hr1', 'hr2', 'hr3', 'hr4', 'hr5', 'hr6', 
                      'hr7', 'hr8', 'hr9', 'hr10', 'hr11', 'hr12', 'hr13', 'hr14', 
                      'hr15', 'hr16', 'hr17', 'hr18', 'hr19', 'hr20', 'hr21', 'hr22', 
                      'hr23', 'hr24']
    
    # 7. Select and return the final dataframe
    # Ensure we only return the specified columns
    return df[target_columns]