import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the Date column
    # Source format is 'Thu 10/01/2009' which is %a %m/%d/%Y
    dt = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # 2. Create 'month' column with full month name (e.g., 'January')
    df['month'] = dt.dt.strftime('%B')
    
    # 3. Create 'daytype' column
    # dayofweek: 0=Monday, ..., 4=Friday, 5=Saturday, 6=Sunday
    # Weekdays are 0-4, Weekends are 5-6
    df['daytype'] = dt.dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # 4. Rename hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'hr{i}'
    # Handle the 24th hour specifically as it has a different format in source
    rename_dict['24:00:00'] = 'hr24'
    
    df = df.rename(columns=rename_dict)
    
    # 5. Define target columns and return
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    return df[target_columns]