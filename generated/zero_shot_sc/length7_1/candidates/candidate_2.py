import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing daily hourly load profiles
    into a target DataFrame with month, daytype, and standardized hour columns.
    """
    df = source.copy()
    
    # 1. Parse the CST column to datetime
    # Format: 'Sat 12/01/2012' -> %a %m/%d/%Y
    df['parsed_date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    
    # 2. Extract 'month' column (Full month name, e.g., 'April')
    df['month'] = df['parsed_date'].dt.strftime('%B')
    
    # 3. Extract 'daytype' column
    # dayofweek: 0=Mon, 1=Tue, ..., 4=Fri, 5=Sat, 6=Sun
    # Weekends are Saturday (5) and Sunday (6)
    df['daytype'] = df['parsed_date'].dt.dayofweek.apply(lambda x: 'weekend' if x >= 5 else 'weekday')
    
    # 4. Rename hour columns to hr1, hr2, ..., hr24
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    
    col_mapping = {}
    for h in range(1, 24):
        col_mapping[f'{h}:00'] = f'hr{h}'
    col_mapping['24:00:00'] = 'hr24'
    
    df = df.rename(columns=col_mapping)
    
    # 5. Define target columns in the correct order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Select and return the final dataframe
    # Ensure all required columns exist and are in the correct order
    return df[target_columns]