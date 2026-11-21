import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format: %m/%d/%Y
    # Target format: %Y-%m-%d %H:%M:%S
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Define the mapping from source hour columns to target value columns
    # Chronological order:
    # 12:00 AM (00:00) -> value1
    # 1:00 AM (01:00) -> value2
    # ...
    # 11:00 AM (11:00) -> value12
    # 12:00 PM (12:00) -> value13
    # 1:00 PM (13:00) -> value14
    # ...
    # 11:00 PM (23:00) -> value24
    
    rename_dict = {
        '12:00 AM': 'value1',
        '1:00 AM': 'value2',
        '2:00 AM': 'value3',
        '3:00 AM': 'value4',
        '4:00 AM': 'value5',
        '5:00 AM': 'value6',
        '6:00 AM': 'value7',
        '7:00 AM': 'value8',
        '8:00 AM': 'value9',
        '9:00 AM': 'value10',
        '10:00 AM': 'value11',
        '11:00 AM': 'value12',
        '12:00 PM': 'value13',
        '1:00 PM': 'value14',
        '2:00 PM': 'value15',
        '3:00 PM': 'value16',
        '4:00 PM': 'value17',
        '5:00 PM': 'value18',
        '6:00 PM': 'value19',
        '7:00 PM': 'value20',
        '8:00 PM': 'value21',
        '9:00 PM': 'value22',
        '10:00 PM': 'value23',
        '11:00 PM': 'value24'
    }
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 4. Return the dataframe with only the target columns
    return df[target_columns]