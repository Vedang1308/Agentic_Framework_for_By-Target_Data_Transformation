import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse and format the date column
    # Source format: %m/%d/%Y (e.g., '7/3/2011')
    # Target format: %Y-%m-%d %H:%M:%S (e.g., '2011-01-01 00:00:00')
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    df['date'] = df['date'].dt.strftime('%Y-%m-%d 00:00:00')
    
    # 2. Define the mapping from source value columns to target hour columns
    # Based on standard hourly data conventions:
    # value1 = 12:00 AM (Midnight)
    # value2 = 1:00 AM
    # ...
    # value12 = 11:00 AM
    # value13 = 12:00 PM (Noon)
    # ...
    # value24 = 11:00 PM
    
    # Target columns list
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    # Create a new dataframe with the date column
    result = pd.DataFrame({'date': df['date']})
    
    # Map values to the specific hour columns
    # 1:00 AM to 11:00 AM correspond to value2 to value12
    for i in range(1, 12):
        hour_str = f'{i}:00 AM'
        result[hour_str] = df[f'value{i+1}']
        
    # 12:00 AM corresponds to value1
    result['12:00 AM'] = df['value1']
    
    # 1:00 PM to 11:00 PM correspond to value14 to value24
    for i in range(1, 12):
        hour_str = f'{i}:00 PM'
        result[hour_str] = df[f'value{i+13}']
        
    # 12:00 PM corresponds to value13
    result['12:00 PM'] = df['value13']
    
    # 3. Ensure the column order matches the target exactly
    result = result[target_columns]
    
    return result