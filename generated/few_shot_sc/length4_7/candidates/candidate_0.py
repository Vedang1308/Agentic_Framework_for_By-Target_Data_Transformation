import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Process the Date column
    # Source format: 'Thu 10/01/2009' (%a %m/%d/%Y)
    # Target format: '01/01/2003' (%m/%d/%Y)
    # Extract the date part after the space
    date_part = df['Date'].str.split(' ').str[-1]
    dt = pd.to_datetime(date_part, format='%m/%d/%Y')
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename hourly columns
    # Mapping from 24-hour format (source) to 12-hour AM/PM format (target)
    rename_dict = {
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
    
    df = df.rename(columns=rename_dict)
    
    # 3. Select and order columns according to target schema
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', 
        '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM', '1:00 PM', '2:00 PM', 
        '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', 
        '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    return df[target_columns]