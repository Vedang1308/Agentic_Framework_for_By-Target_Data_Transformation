import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the mapping from source hourly columns to target value columns
    # Chronological order: 12:00 AM is value1, 1:00 AM is value2, ..., 11:00 PM is value24
    col_mapping = {
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
    
    # Rename the columns
    df = source.rename(columns=col_mapping)
    
    # Parse the date column and format it to the target format
    # Source format: '%m/%d/%Y'
    # Target format: '%Y-%m-%d %H:%M:%S'
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define the target columns in the correct order
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # Select only the target columns
    # Note: The DSL column is dropped as it is not in the target schema
    df = df[target_columns]
    
    # Ensure the output types match expectations (date is object/string, values are float)
    # The values are already float64 from the source.
    # The date is now string object.
    
    return df[target_columns]