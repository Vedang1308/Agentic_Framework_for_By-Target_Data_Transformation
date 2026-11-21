import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the target columns verbatim
    target_columns = [
        'Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 
        'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 
        'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24'
    ]
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format is MM/DD/YYYY, Target format is YYYY-MM-DD HH:MM:SS
    df['Date'] = pd.to_datetime(df['date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Define mapping from source hour columns to target hour columns
    # Source order in schema: 1AM, 2AM, ..., 11AM, 12AM, 1PM, ..., 12PM
    # Logical order (Hr 1 to Hr 24):
    # Hr 1: 12:00 AM (00:00)
    # Hr 2: 1:00 AM (01:00)
    # ...
    # Hr 12: 11:00 AM (11:00)
    # Hr 13: 12:00 PM (12:00)
    # ...
    # Hr 24: 11:00 PM (23:00)
    
    rename_map = {
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
    
    # 3. Rename the columns
    df.rename(columns=rename_map, inplace=True)
    
    # 4. Select only the target columns
    # This automatically drops 'date' and 'DSL' and any other unwanted columns
    df = df[target_columns]
    
    # 5. Sort by Date to match the target sample order (chronological)
    df.sort_values(by='Date', inplace=True)
    
    # 6. Reset index
    df.reset_index(drop=True, inplace=True)
    
    return df[target_columns]