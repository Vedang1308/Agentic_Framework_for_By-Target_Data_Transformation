import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date from the 'CST' column
    # Source format: '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # We need to extract the date part and format it as '%m/%d/%Y'
    # pd.to_datetime can handle the full string, but let's be safe with parsing
    # The day of week part is not needed for the output date, but helps parsing if ambiguous.
    # However, standard pd.to_datetime handles 'Sat 12/01/2012' correctly.
    dt = pd.to_datetime(df['CST'])
    
    # 2. Create the 'Date' column with format '%m/%d/%Y'
    df['Date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 3. Rename hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hr {i}'
    
    # Handle the 24th hour specifically because of the '24:00:00' format
    if '24:00:00' in df.columns:
        rename_dict['24:00:00'] = 'Hr 24'
    elif '24:00' in df.columns:
        rename_dict['24:00'] = 'Hr 24'
        
    df = df.rename(columns=rename_dict)
    
    # 4. Define the target columns in the correct order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 5. Return the dataframe with only the target columns
    return df[target_columns]