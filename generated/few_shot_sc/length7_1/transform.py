import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the CST column to datetime
    # Format is 'Sat 12/01/2012' -> '%a %m/%d/%Y'
    # We need to handle the fact that the day name is abbreviated.
    dt = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    
    # 2. Create 'month' column with full month name
    df['month'] = dt.dt.strftime('%B')
    
    # 3. Create 'daytype' column
    # Monday=0, Tuesday=1, ..., Friday=4, Saturday=5, Sunday=6
    # Weekday if 0-4, Weekend if 5-6
    dayofweek = dt.dt.dayofweek
    df['daytype'] = dayofweek.apply(lambda x: 'weekend' if x >= 5 else 'weekday')
    
    # 4. Rename hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    rename_dict = {}
    for i in range(1, 25):
        src_col = f'{i}:00'
        if i == 24:
            src_col = '24:00:00'
        tgt_col = f'hr{i}'
        if src_col in df.columns:
            rename_dict[src_col] = tgt_col
            
    df = df.rename(columns=rename_dict)
    
    # 5. Define target columns in order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Return the dataframe with only the target columns
    return df[target_columns]