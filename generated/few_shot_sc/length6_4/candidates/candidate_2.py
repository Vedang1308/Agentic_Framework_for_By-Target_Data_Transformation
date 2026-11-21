import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Format the Date column
    # Source format: 'M/D/YYYY' (e.g., '7/3/2014')
    # Target format: 'YYYY-MM-DD 00:00:00'
    df['Date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d 00:00:00')
    
    # 2. Map hour columns
    # Source columns are '12:00 AM', '1:00 AM', ..., '11:00 PM'
    # Target columns are 'Hr 1', 'Hr 2', ..., 'Hr 24'
    # Mapping logic:
    # 12:00 AM -> Hr 1
    # 1:00 AM -> Hr 2
    # ...
    # 11:00 AM -> Hr 12
    # 12:00 PM -> Hr 13
    # 1:00 PM -> Hr 14
    # ...
    # 11:00 PM -> Hr 24
    
    rename_map = {}
    
    # AM Hours: 12:00 AM is Hr 1, 1:00 AM is Hr 2, ..., 11:00 AM is Hr 12
    # Note: 12:00 AM is the first hour of the day in this context.
    am_hours = ['12:00 AM', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', 
                '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM']
    for i, col in enumerate(am_hours, start=1):
        rename_map[col] = f'Hr {i}'
        
    # PM Hours: 12:00 PM is Hr 13, 1:00 PM is Hr 14, ..., 11:00 PM is Hr 24
    pm_hours = ['12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', 
                '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM']
    for i, col in enumerate(pm_hours, start=13):
        rename_map[col] = f'Hr {i}'
        
    df = df.rename(columns=rename_map)
    
    # 3. Define target columns
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Select and return
    # Ensure we only return the required columns
    return df[target_columns]