import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the mapping from source hourly columns to target hourly columns
    # Source 1:00-11:00 are AM hours 1-11
    # Source 12:00 is 12 PM
    # Source 13:00-23:00 are PM hours 1-11
    # Source 24:00:00 is 12 AM
    
    col_mapping = {
        '1:00': '1:00 AM',
        '2:00': '2:00 AM',
        '3:00': '3:00 AM',
        '4:00': '4:00 AM',
        '5:00': '5:00 AM',
        '6:00': '6:00 AM',
        '7:00': '7:00 AM',
        '8:00': '8:00 AM',
        '9:00': '9:00 AM',
        '10:00': '10:00 AM',
        '11:00': '11:00 AM',
        '12:00': '12:00 PM',
        '13:00': '1:00 PM',
        '14:00': '2:00 PM',
        '15:00': '3:00 PM',
        '16:00': '4:00 PM',
        '17:00': '5:00 PM',
        '18:00': '6:00 PM',
        '19:00': '7:00 PM',
        '20:00': '8:00 PM',
        '21:00': '9:00 PM',
        '22:00': '10:00 PM',
        '23:00': '11:00 PM',
        '24:00:00': '12:00 AM'
    }
    
    # Start with a copy of the source dataframe
    df = source.copy()
    
    # Drop the Segment column as it is not in the target
    df = df.drop(columns=['Segment'])
    
    # Transform the Date column
    # Source format: 'Thu 10/01/2009'
    # Target format: '01/01/2003' (MM/DD/YYYY)
    # We can split by space and take the second part, or parse and format.
    # Parsing is robust:
    df['date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    df = df.drop(columns=['Date'])
    
    # Rename the hourly columns
    df = df.rename(columns=col_mapping)
    
    # Define the exact target column order as specified in the problem description
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', 
        '12:00 PM'
    ]
    
    # Select and order the columns
    df = df[target_columns]
    
    return df