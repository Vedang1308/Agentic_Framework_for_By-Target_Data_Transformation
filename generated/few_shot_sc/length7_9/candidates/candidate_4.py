import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the Date column
    # Source format is like 'Thu 10/01/2009'
    dt = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # 2. Create 'month' column with full month name
    df['month'] = dt.dt.strftime('%B')
    
    # 3. Create 'daytype' column
    # 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday, 6=Sunday
    # Weekend is Saturday (5) or Sunday (6)
    df['daytype'] = dt.dt.dayofweek.map({
        0: 'weekday',
        1: 'weekday',
        2: 'weekday',
        3: 'weekday',
        4: 'weekday',
        5: 'weekend',
        6: 'weekend'
    })
    
    # 4. Rename hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'hr{i}'
    rename_dict['24:00:00'] = 'hr24'
    
    df = df.rename(columns=rename_dict)
    
    # 5. Define target columns verbatim
    target_cols = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Return the transformed dataframe
    return df[target_cols]