import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date from the CST column
    # CST format is '%a %m/%d/%Y', e.g., 'Sat 12/01/2012'
    # Extract the date part (last element after splitting by space)
    date_str = df['CST'].str.split(' ').str[-1]
    dt = pd.to_datetime(date_str, format='%m/%d/%Y')
    
    # 2. Create 'month' column with full month name
    df['month'] = dt.dt.strftime('%B')
    
    # 3. Create 'daytype' column
    # dayofweek: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    # Weekday if 0-4, Weekend if 5-6
    df['daytype'] = dt.dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # 4. Rename hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'hr{i}'
    rename_dict['24:00:00'] = 'hr24'
    
    df = df.rename(columns=rename_dict)
    
    # 5. Define target columns
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Return the transformed dataframe with exact column order
    return df[target_columns]