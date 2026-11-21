import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    
    Steps:
    1. Parse the 'date' column from '%m/%d/%Y' to datetime.
    2. Format the date to '%Y-%m-%d %H:%M:%S' (with time 00:00:00).
    3. Map the 24 hourly columns (AM/PM format) to 'Hr 1' through 'Hr 24'.
       - 12:00 AM -> Hr 1
       - 1:00 AM  -> Hr 2
       - ...
       - 12:00 PM -> Hr 13
       - ...
       - 11:00 PM -> Hr 24
    4. Drop the 'DSL' column.
    5. Reorder columns to match target schema.
    """
    
    # 1. Create a copy to avoid modifying the original
    df = source.copy()
    
    # 2. Parse and format the date
    # Source format: %m/%d/%Y
    # Target format: %Y-%m-%d %H:%M:%S
    df['Date'] = pd.to_datetime(df['date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 3. Define the mapping from source hourly columns to target hourly columns
    # Mapping logic:
    # 12 AM is the start of the day (Hour 1)
    # 1 AM is Hour 2
    # ...
    # 11 AM is Hour 12
    # 12 PM is Noon (Hour 13)
    # 1 PM is Hour 14
    # ...
    # 11 PM is Hour 24
    
    col_mapping = {
        '12:00 AM': 'Hr 1',
        '1:00 AM': 'Hr 2',
        '2:00 AM': 'Hr 3',
        '3:00 AM': 'Hr 4',
        '4:00 AM': 'Hr 5',
        '5:00 AM': 'Hr 6',
        '6:00 AM': 'Hr 7',
        '7:00 AM': 'Hr 8',
        '8:00 AM': 'Hr 9',
        '9:00 AM': 'Hr 10',
        '10:00 AM': 'Hr 11',
        '11:00 AM': 'Hr 12',
        '12:00 PM': 'Hr 13',
        '1:00 PM': 'Hr 14',
        '2:00 PM': 'Hr 15',
        '3:00 PM': 'Hr 16',
        '4:00 PM': 'Hr 17',
        '5:00 PM': 'Hr 18',
        '6:00 PM': 'Hr 19',
        '7:00 PM': 'Hr 20',
        '8:00 PM': 'Hr 21',
        '9:00 PM': 'Hr 22',
        '10:00 PM': 'Hr 23',
        '11:00 PM': 'Hr 24'
    }
    
    # Rename the hourly columns
    df.rename(columns=col_mapping, inplace=True)
    
    # 4. Define the target column order
    target_columns = ['Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24']
    
    # 5. Select only the required columns (this effectively drops 'date' and 'DSL')
    df = df[target_columns]
    
    # 6. Reset index to ensure clean integer index
    df.reset_index(drop=True, inplace=True)
    
    return df[target_columns]