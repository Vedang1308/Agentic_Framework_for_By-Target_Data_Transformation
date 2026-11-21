import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the target columns in the exact order required
    target_columns = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    # Create a copy of the source to avoid modifying the original
    df = source.copy()
    
    # 1. Transform the Date column
    # Source format: '%a %m/%d/%Y' (e.g., 'Thu 10/01/2009')
    # Target format: '%m/%d/%Y' (e.g., '10/01/2009')
    df['date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Map source time columns to target time columns
    # Mapping logic:
    # 1:00 - 11:00 -> 1:00 AM - 11:00 AM
    # 12:00 -> 12:00 PM (Noon)
    # 13:00 - 23:00 -> 1:00 PM - 11:00 PM
    # 24:00:00 -> 12:00 AM (Midnight)
    
    column_mapping = {
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
    
    df = df.rename(columns=column_mapping)
    
    # 3. Select and order the columns as per the target schema
    # Drop the original 'Date' and 'Segment' columns if they still exist, 
    # by explicitly selecting only the target columns.
    return df[target_columns]