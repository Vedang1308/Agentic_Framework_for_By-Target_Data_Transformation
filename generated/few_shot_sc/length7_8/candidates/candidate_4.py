import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and extract month and daytype
    dt = pd.to_datetime(df['Date'])
    df['month'] = dt.dt.strftime('%B')
    
    # Determine daytype: weekday (Mon-Fri) or weekend (Sat-Sun)
    # dayofweek: 0=Monday, ..., 4=Friday, 5=Saturday, 6=Sunday
    df['daytype'] = dt.dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # 2. Rename hourly columns from 'Hr 1'...'Hr 24' to 'hr1'...'hr24'
    rename_dict = {}
    for i in range(1, 25):
        old_col = f'Hr {i}'
        new_col = f'hr{i}'
        if old_col in df.columns:
            rename_dict[old_col] = new_col
            
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in the correct order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 4. Select and return the target columns
    return df[target_columns]