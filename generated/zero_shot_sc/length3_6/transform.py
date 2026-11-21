import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format: %m/%d/%Y
    # Target format: %Y-%m-%d %H:%M:%S
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Define the mapping from source column names to target column names
    # Source columns represent the hour ending at that time? Or starting?
    # Standard convention: "1:00 AM" column usually represents the data for the hour 00:00-01:00? 
    # Or is it the value AT 1:00 AM?
    # Let's look at the mapping again.
    # Hour 1 in 24h clock is 00:00-01:00. This corresponds to 12:00 AM in 12h clock.
    # Hour 2 in 24h clock is 01:00-02:00. This corresponds to 1:00 AM in 12h clock.
    # ...
    # Hour 13 in 24h clock is 12:00-13:00. This corresponds to 12:00 PM in 12h clock.
    # Hour 14 in 24h clock is 13:00-14:00. This corresponds to 1:00 PM in 12h clock.
    
    mapping = {
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
    
    # 3. Rename the columns
    df = df.rename(columns=mapping)
    
    # 4. Select only the required columns for the target
    # The target schema has 'date' followed by 'Hour 1' to 'Hour 24'
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 5. Sort by date to ensure consistent ordering (as seen in target sample)
    df = df.sort_values(by='date').reset_index(drop=True)
    
    # 6. Return the DataFrame with exact target columns
    return df[target_columns]