import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with daily hourly profiles into a target DataFrame
    with columns: month, daytype, hr1...hr24.
    """
    df = source.copy()
    
    # 1. Parse the 'CST' column to datetime
    # Format: '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    df['datetime'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    
    # 2. Extract 'month' as full name (e.g., 'April', 'November')
    df['month'] = df['datetime'].dt.strftime('%B')
    
    # 3. Extract 'daytype'
    # dayofweek: 0=Monday, ..., 4=Friday, 5=Saturday, 6=Sunday
    df['daytype'] = df['datetime'].dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # 4. Rename the hour columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    
    col_mapping = {}
    for i in range(1, 24):
        col_mapping[f'{i}:00'] = f'hr{i}'
    col_mapping['24:00:00'] = 'hr24'
    
    df = df.rename(columns=col_mapping)
    
    # 5. Select and order the target columns
    target_columns = ['month', 'daytype', 'hr1', 'hr2', 'hr3', 'hr4', 'hr5', 'hr6', 'hr7', 'hr8', 'hr9', 'hr10', 'hr11', 'hr12', 'hr13', 'hr14', 'hr15', 'hr16', 'hr17', 'hr18', 'hr19', 'hr20', 'hr21', 'hr22', 'hr23', 'hr24']
    
    # Ensure the columns exist and select them
    # Note: If any hour column is missing in source, this will raise KeyError, 
    # which is appropriate for schema mismatch.
    df = df[target_columns]
    
    # Reset index to ensure clean output
    df = df.reset_index(drop=True)
    
    return df[target_columns]