import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the Date column
    # Format is '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    # We need to handle the parsing carefully. pd.to_datetime usually handles this, 
    # but let's ensure robustness by splitting if necessary or using format.
    # The sample shows 'Thu 10/01/2009'. 
    dt_series = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # 2. Extract 'month' as full name (e.g., 'January')
    df['month'] = dt_series.dt.strftime('%B')
    
    # 3. Determine 'daytype'
    # dayofweek: 0=Monday, ..., 4=Friday, 5=Saturday, 6=Sunday
    # weekday: 0-4, weekend: 5-6
    is_weekend = dt_series.dt.dayofweek >= 5
    df['daytype'] = is_weekend.map({True: 'weekend', False: 'weekday'})
    
    # 4. Rename hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'hr{i}'
    rename_dict['24:00:00'] = 'hr24'
    
    df = df.rename(columns=rename_dict)
    
    # 5. Define target columns and return
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    return df[target_columns]