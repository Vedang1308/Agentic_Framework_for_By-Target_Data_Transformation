import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the CST column to datetime
    # Source format: 'Sat 12/01/2012' -> '%a %m/%d/%Y'
    # We use format='%a %m/%d/%Y' to parse strictly
    dt = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    
    # 2. Create the 'date' column in target format '%m/%d/%Y'
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 3. Rename the hour columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'Hour 1', 'Hour 2', ..., 'Hour 23', 'Hour 24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hour {i}'
    # Handle the specific 24th hour column name
    if '24:00:00' in df.columns:
        rename_dict['24:00:00'] = 'Hour 24'
    elif '24:00' in df.columns:
        rename_dict['24:00'] = 'Hour 24'
        
    df = df.rename(columns=rename_dict)
    
    # 4. Sort by date to match target sample order (ascending)
    # Sorting by the string 'MM/DD/YYYY' works correctly for chronological order
    df = df.sort_values(by='date', ascending=True).reset_index(drop=True)
    
    # 5. Define target columns verbatim
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 6. Return the transformed dataframe with only target columns
    return df[target_columns]