import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the target column names verbatim
    target_columns = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', 
        '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 AM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', 
        '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', 
        '12:00 PM'
    ]
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Rename the 'Date' column to 'date'
    df = df.rename(columns={'Date': 'date'})
    
    # Define the mapping from source numeric columns to target time labels
    # Source columns are strings '1' through '24'
    col_mapping = {
        '1': '1:00 AM',
        '2': '2:00 AM',
        '3': '3:00 AM',
        '4': '4:00 AM',
        '5': '5:00 AM',
        '6': '6:00 AM',
        '7': '7:00 AM',
        '8': '8:00 AM',
        '9': '9:00 AM',
        '10': '10:00 AM',
        '11': '11:00 AM',
        '24': '12:00 AM',  # Midnight
        '13': '1:00 PM',
        '14': '2:00 PM',
        '15': '3:00 PM',
        '16': '4:00 PM',
        '17': '5:00 PM',
        '18': '6:00 PM',
        '19': '7:00 PM',
        '20': '8:00 PM',
        '21': '9:00 PM',
        '22': '10:00 PM',
        '23': '11:00 PM',
        '12': '12:00 PM'   # Noon
    }
    
    # Apply the column renaming
    df = df.rename(columns=col_mapping)
    
    # Select and reorder columns to match the target schema exactly
    # Ensure 'date' is the first column, followed by the time columns in the specified order
    df = df[target_columns]
    
    return df[target_columns]