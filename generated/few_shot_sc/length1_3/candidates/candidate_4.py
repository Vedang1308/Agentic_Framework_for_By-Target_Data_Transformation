import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform the date column 'date' to 'cst'
    # Source format: %m/%d/%Y (e.g., '7/3/2014')
    # Target format: %a %m/%d/%Y (e.g., 'Wed 01/01/2014')
    df['date_parsed'] = pd.to_datetime(df['date'])
    df['cst'] = df['date_parsed'].dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename the hourly columns from AM/PM format to 24-hour format
    # Mapping logic:
    # 1:00 AM -> 1:00, ..., 11:00 AM -> 11:00
    # 12:00 PM -> 12:00
    # 1:00 PM -> 13:00, ..., 11:00 PM -> 23:00
    # 12:00 AM -> 24:00
    
    rename_map = {
        '1:00 AM': '1:00',
        '2:00 AM': '2:00',
        '3:00 AM': '3:00',
        '4:00 AM': '4:00',
        '5:00 AM': '5:00',
        '6:00 AM': '6:00',
        '7:00 AM': '7:00',
        '8:00 AM': '8:00',
        '9:00 AM': '9:00',
        '10:00 AM': '10:00',
        '11:00 AM': '11:00',
        '12:00 PM': '12:00',
        '1:00 PM': '13:00',
        '2:00 PM': '14:00',
        '3:00 PM': '15:00',
        '4:00 PM': '16:00',
        '5:00 PM': '17:00',
        '6:00 PM': '18:00',
        '7:00 PM': '19:00',
        '8:00 PM': '20:00',
        '9:00 PM': '21:00',
        '10:00 PM': '22:00',
        '11:00 PM': '23:00',
        '12:00 AM': '24:00'
    }
    
    df = df.rename(columns=rename_map)
    
    # 3. Define the target columns in the correct order
    # First 'cst', then hours 1:00 to 24:00
    hour_cols = [f'{i}:00' for i in range(1, 25)]
    target_columns = ['cst'] + hour_cols
    
    # 4. Select only the required columns
    # Note: We drop 'date', 'date_parsed', and 'DSL' implicitly by selecting only target_columns
    return df[target_columns]