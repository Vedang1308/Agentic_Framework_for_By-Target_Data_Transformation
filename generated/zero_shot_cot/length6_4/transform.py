import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the mapping from source column names to target column names
    # Source columns are in 12-hour format, target are Hr 1 to Hr 24
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
    
    # Create a copy of the source dataframe to avoid modifying the original
    df = source.copy()
    
    # Select only the date and the hourly columns
    # The hourly columns are the keys in our mapping
    hourly_cols = list(col_mapping.keys())
    cols_to_keep = ['date'] + hourly_cols
    
    # Ensure all required columns exist in the source
    # In case of any missing columns, we should handle it, but assuming valid input
    df = df[cols_to_keep]
    
    # Rename the hourly columns
    df = df.rename(columns=col_mapping)
    
    # Parse the date column
    # Source format is '%m/%d/%Y'
    df['Date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # Format the date column to '%Y-%m-%d %H:%M:%S'
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Drop the original 'date' column
    df = df.drop(columns=['date'])
    
    # Define the target column order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # Ensure the columns are in the correct order
    df = df[target_columns]
    
    return df[target_columns]