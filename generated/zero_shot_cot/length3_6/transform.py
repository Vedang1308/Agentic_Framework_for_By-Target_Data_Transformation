import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the mapping from source hour columns to target hour columns
    # 12:00 AM is the first hour (Hour 1), 1:00 AM is the second (Hour 2), etc.
    # 12:00 PM is the 13th hour (Hour 13), 1:00 PM is the 14th (Hour 14), etc.
    hour_mapping = {
        '12:00 AM': 'Hour 1',
        '1:00 AM': 'Hour 2',
        '2:00 AM': 'Hour 3',
        '3:00 AM': 'Hour 4',
        '4:00 AM': 'Hour 5',
        '5:00 AM': 'Hour 6',
        '6:00 AM': 'Hour 7',
        '7:00 AM': 'Hour 8',
        '8:00 AM': 'Hour 9',
        '9:00 AM': 'Hour 10',
        '10:00 AM': 'Hour 11',
        '11:00 AM': 'Hour 12',
        '12:00 PM': 'Hour 13',
        '1:00 PM': 'Hour 14',
        '2:00 PM': 'Hour 15',
        '3:00 PM': 'Hour 16',
        '4:00 PM': 'Hour 17',
        '5:00 PM': 'Hour 18',
        '6:00 PM': 'Hour 19',
        '7:00 PM': 'Hour 20',
        '8:00 PM': 'Hour 21',
        '9:00 PM': 'Hour 22',
        '10:00 PM': 'Hour 23',
        '11:00 PM': 'Hour 24'
    }
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Rename the hour columns
    df.rename(columns=hour_mapping, inplace=True)
    
    # Drop the DSL column as it is not in the target
    if 'DSL' in df.columns:
        df.drop(columns=['DSL'], inplace=True)
    
    # Parse and format the date column
    # Source format: '%m/%d/%Y'
    # Target format: '%Y-%m-%d %H:%M:%S'
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define the target column order
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # Ensure the DataFrame has the correct columns in the correct order
    # If any hour columns are missing (unlikely given the schema), this will raise an error
    # which is appropriate for debugging.
    df = df[target_columns]
    
    return df