import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format: '%m/%d/%Y'
    # Target format: '%Y-%m-%d %H:%M:%S'
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Define the mapping from source hour columns to target time labels
    # Hour 1-11: 1:00 AM - 11:00 AM
    # Hour 12: 12:00 PM
    # Hour 13-23: 1:00 PM - 11:00 PM
    # Hour 24: 12:00 AM
    
    rename_map = {}
    for h in range(1, 12):
        rename_map[f'Hour {h}'] = f'{h}:00 AM'
    
    rename_map['Hour 12'] = '12:00 PM'
    
    for h in range(13, 24):
        pm_hour = h - 12
        rename_map[f'Hour {h}'] = f'{pm_hour}:00 PM'
        
    rename_map['Hour 24'] = '12:00 AM'
    
    # 3. Rename the columns
    df = df.rename(columns=rename_map)
    
    # 4. Define the exact target column order
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', 
        '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', 
        '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    # 5. Select and reorder columns to match target schema
    # Ensure all target columns exist in df
    for col in target_columns:
        if col not in df.columns:
            raise ValueError(f"Column {col} not found in transformed dataframe")
            
    df = df[target_columns]
    
    return df