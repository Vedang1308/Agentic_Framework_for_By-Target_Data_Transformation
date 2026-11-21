import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and reformat the date column
    # Source format: '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # Target format: '%m/%d/%Y' (e.g., '12/01/2012')
    # We can parse directly since pd.to_datetime handles '%a %m/%d/%Y' reasonably well if we specify format or infer.
    # Explicitly splitting is safer if the day name varies in length or locale, but standard English day names are fixed.
    # Let's try parsing the whole string.
    dt = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    df['Date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hr {i}'
    # Handle the 24th hour specifically as it has ':00:00'
    rename_dict['24:00:00'] = 'Hr 24'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns verbatim
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Return the transformed dataframe with only target columns
    return df[target_columns]