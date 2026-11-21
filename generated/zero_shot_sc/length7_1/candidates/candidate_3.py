import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the CST column to extract date information
    # Format: 'Sat 12/01/2012' -> '%a %m/%d/%Y'
    df['parsed_date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    
    # 2. Extract 'month' as full name (e.g., 'April')
    df['month'] = df['parsed_date'].dt.strftime('%B')
    
    # 3. Extract 'daytype'
    # weekday() returns 0-6 for Mon-Sun. 0-4 are weekdays, 5-6 are weekends.
    df['daytype'] = df['parsed_date'].dt.weekday.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # 4. Rename hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    
    rename_map = {}
    for i in range(1, 24):
        rename_map[f'{i}:00'] = f'hr{i}'
    rename_map['24:00:00'] = 'hr24'
    
    df = df.rename(columns=rename_map)
    
    # 5. Define target columns in the exact order required
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Select and return the target columns
    # Drop the helper column 'parsed_date' and 'CST' implicitly by selection
    return df[target_columns]