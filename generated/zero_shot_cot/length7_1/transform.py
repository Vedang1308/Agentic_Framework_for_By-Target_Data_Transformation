import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with daily hourly load profiles into a target DataFrame
    with explicit month, daytype, and renamed hourly columns.
    """
    df = source.copy()
    
    # 1. Parse the CST column to datetime
    # Format is '%a %m/%d/%Y' e.g., 'Sat 12/01/2012'
    df['CST_dt'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    
    # 2. Extract 'month' as full name (e.g., 'December', 'April')
    df['month'] = df['CST_dt'].dt.strftime('%B')
    
    # 3. Extract 'daytype'
    # dayofweek: 0=Monday, ..., 4=Friday, 5=Saturday, 6=Sunday
    # Weekdays: 0-4, Weekends: 5-6
    df['daytype'] = df['CST_dt'].dt.dayofweek.apply(
        lambda x: 'weekday' if x < 5 else 'weekend'
    )
    
    # 4. Rename the hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    rename_map = {}
    for i in range(1, 24):
        rename_map[f'{i}:00'] = f'hr{i}'
    rename_map['24:00:00'] = 'hr24'
    
    df = df.rename(columns=rename_map)
    
    # 5. Define the target column order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Select and return the required columns
    # Drop the temporary datetime column and original CST if not already handled by selection
    df = df[target_columns]
    
    return df