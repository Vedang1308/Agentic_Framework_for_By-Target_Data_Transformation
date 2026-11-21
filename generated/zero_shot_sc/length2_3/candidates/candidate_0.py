import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid SettingWithCopyWarning
    df = source.copy()
    
    # 1. Parse the date column
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Create dt_strata: Format date as M/D/YYYY without leading zeros
    # strftime produces MM/DD/YYYY, so we strip leading zeros from the whole string 
    # effectively removing the leading zero of single-digit months and days.
    # '07/03/2014' -> '7/3/2014'
    # '10/10/2014' -> '10/10/2014'
    df['dt_strata'] = df['date_parsed'].dt.strftime('%m/%d/%Y').str.lstrip('0')
    
    # 3. Create dow: Sunday=0, Monday=1, ..., Saturday=6
    # Python weekday: Monday=0, ..., Sunday=6
    # Transformation: (weekday + 1) % 7
    df['dow'] = (df['date_parsed'].dt.weekday + 1) % 7
    
    # 4. Map hourly columns
    # Source columns are strings like '1:00 AM', '12:00 PM', etc.
    # Target columns are 'pct_hourly_0100', ..., 'pct_hourly_2400'
    
    # Define the mapping based on chronological order of hours
    # 1:00 AM -> 0100
    # 2:00 AM -> 0200
    # ...
    # 11:00 AM -> 1100
    # 12:00 PM -> 1200
    # 1:00 PM -> 1300
    # ...
    # 11:00 PM -> 2300
    # 12:00 AM -> 2400
    
    hour_mapping = {
        '1:00 AM': 'pct_hourly_0100',
        '2:00 AM': 'pct_hourly_0200',
        '3:00 AM': 'pct_hourly_0300',
        '4:00 AM': 'pct_hourly_0400',
        '5:00 AM': 'pct_hourly_0500',
        '6:00 AM': 'pct_hourly_0600',
        '7:00 AM': 'pct_hourly_0700',
        '8:00 AM': 'pct_hourly_0800',
        '9:00 AM': 'pct_hourly_0900',
        '10:00 AM': 'pct_hourly_1000',
        '11:00 AM': 'pct_hourly_1100',
        '12:00 PM': 'pct_hourly_1200',
        '1:00 PM': 'pct_hourly_1300',
        '2:00 PM': 'pct_hourly_1400',
        '3:00 PM': 'pct_hourly_1500',
        '4:00 PM': 'pct_hourly_1600',
        '5:00 PM': 'pct_hourly_1700',
        '6:00 PM': 'pct_hourly_1800',
        '7:00 PM': 'pct_hourly_1900',
        '8:00 PM': 'pct_hourly_2000',
        '9:00 PM': 'pct_hourly_2100',
        '10:00 PM': 'pct_hourly_2200',
        '11:00 PM': 'pct_hourly_2300',
        '12:00 AM': 'pct_hourly_2400',
    }
    
    df.rename(columns=hour_mapping, inplace=True)
    
    # 5. Map DSL to pct_hourly_2500
    df.rename(columns={'DSL': 'pct_hourly_2500'}, inplace=True)
    df['pct_hourly_2500'] = df['pct_hourly_2500'].astype(int)
    
    # 6. Define target column order
    target_columns = [
        'dt_strata', 'dow', 
        'pct_hourly_0100', 'pct_hourly_0200', 'pct_hourly_0300', 'pct_hourly_0400', 
        'pct_hourly_0500', 'pct_hourly_0600', 'pct_hourly_0700', 'pct_hourly_0800', 
        'pct_hourly_0900', 'pct_hourly_1000', 'pct_hourly_1100', 'pct_hourly_1200', 
        'pct_hourly_1300', 'pct_hourly_1400', 'pct_hourly_1500', 'pct_hourly_1600', 
        'pct_hourly_1700', 'pct_hourly_1800', 'pct_hourly_1900', 'pct_hourly_2000', 
        'pct_hourly_2100', 'pct_hourly_2200', 'pct_hourly_2300', 'pct_hourly_2400', 
        'pct_hourly_2500'
    ]
    
    # 7. Select and return the target columns
    # Drop the temporary parsed date column if it's not in target_columns (it isn't)
    df = df.drop(columns=['date', 'date_parsed'])
    
    return df[target_columns]