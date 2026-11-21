import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Define the mapping from source column names to target column names
    # Based on logical hour of the day:
    # 12:00 AM is the start of the day (Hour 1 in 1-24 indexing for values)
    # 1:00 AM is the second hour, etc.
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
    
    # Rename the hourly columns
    df = df.rename(columns=rename_dict)
    
    # Parse the date column and format it to 'YYYY-MM-DD HH:MM:SS'
    # Source format is M/D/YYYY
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define the target columns in the required order
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # Select and return only the target columns
    return df[target_columns]