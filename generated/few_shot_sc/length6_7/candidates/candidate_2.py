import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Handle the Date column
    # The source date format is '%a %m/%d/%Y' (e.g., 'Thu 10/01/2009')
    # The target date format is also '%a %m/%d/%Y'
    # We parse and re-format to ensure consistency and clean data
    df['Date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y').dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename hourly columns
    # Source: '1:00', ..., '23:00', '24:00:00'
    # Target: 'Hr 1', ..., 'Hr 23', 'Hr 24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hr {i}'
    rename_dict['24:00:00'] = 'Hr 24'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns and return
    target_cols = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    return df[target_cols]