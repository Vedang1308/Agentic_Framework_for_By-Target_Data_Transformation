import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format: '%m/%d/%Y'
    # Target format: '%Y-%m-%d %H:%M:%S'
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Define the mapping from source value columns to target time columns
    # Standard hourly data mapping:
    # value1 = 12:00 AM (00:00)
    # value2 = 1:00 AM (01:00)
    # ...
    # value12 = 11:00 AM (11:00)
    # value13 = 12:00 PM (12:00)
    # ...
    # value24 = 11:00 PM (23:00)
    
    column_mapping = {
        'value1': '12:00 AM',
        'value2': '1:00 AM',
        'value3': '2:00 AM',
        'value4': '3:00 AM',
        'value5': '4:00 AM',
        'value6': '5:00 AM',
        'value7': '6:00 AM',
        'value8': '7:00 AM',
        'value9': '8:00 AM',
        'value10': '9:00 AM',
        'value11': '10:00 AM',
        'value12': '11:00 AM',
        'value13': '12:00 PM',
        'value14': '1:00 PM',
        'value15': '2:00 PM',
        'value16': '3:00 PM',
        'value17': '4:00 PM',
        'value18': '5:00 PM',
        'value19': '6:00 PM',
        'value20': '7:00 PM',
        'value21': '8:00 PM',
        'value22': '9:00 PM',
        'value23': '10:00 PM',
        'value24': '11:00 PM'
    }
    
    # 3. Rename the value columns
    df = df.rename(columns=column_mapping)
    
    # 4. Define the target column order verbatim
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', 
        '12:00 PM'
    ]
    
    # 5. Select and reorder columns to match target schema
    # Ensure all target columns exist in the dataframe
    df = df[target_columns]
    
    return df