import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the Date column
    # Source format: 'Thu 10/01/2009'
    # Extract the date part (second element after splitting by space)
    date_str = df['Date'].str.split(' ').str[1]
    dt = pd.to_datetime(date_str, format='%m/%d/%Y')
    
    # 2. Create 'month' column
    # Format as full month name (e.g., 'October')
    df['month'] = dt.dt.strftime('%B')
    
    # 3. Create 'daytype' column
    # dayofweek: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    # Weekend if dayofweek is 5 or 6
    is_weekend = dt.dt.dayofweek.isin([5, 6])
    df['daytype'] = is_weekend.map({True: 'weekend', False: 'weekday'})
    
    # 4. Rename hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'hr{i}'
    # Handle the 24th hour specifically due to format difference
    rename_dict['24:00:00'] = 'hr24'
    
    df = df.rename(columns=rename_dict)
    
    # 5. Define target columns and return
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    return df[target_columns]