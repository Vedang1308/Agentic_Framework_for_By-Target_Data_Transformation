import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date column to extract month and day of week
    # The format is '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    # We can parse it directly or split it. pd.to_datetime handles this well.
    dt = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # Extract full month name (e.g., 'January')
    df['month'] = dt.dt.strftime('%B')
    
    # Determine daytype: weekday (Mon-Fri) or weekend (Sat-Sun)
    # dayofweek: Mon=0, ..., Fri=4, Sat=5, Sun=6
    df['daytype'] = df['daytype'] # placeholder, will overwrite
    df['daytype'] = dt.dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # 2. Rename hour columns
    # Source: 1:00, 2:00, ..., 23:00, 24:00:00
    # Target: hr1, hr2, ..., hr23, hr24
    
    rename_map = {}
    for i in range(1, 24):
        rename_map[f'{i}:00'] = f'hr{i}'
    rename_map['24:00:00'] = 'hr24'
    
    df = df.rename(columns=rename_map)
    
    # 3. Select target columns in the correct order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    return df[target_columns]