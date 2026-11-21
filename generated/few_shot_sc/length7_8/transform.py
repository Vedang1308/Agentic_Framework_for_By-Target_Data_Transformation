import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the Date column
    dt = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Create 'month' column with full month name
    df['month'] = dt.dt.strftime('%B')
    
    # 3. Create 'daytype' column: 'weekday' or 'weekend'
    # dt.weekday: 0=Monday, ..., 4=Friday, 5=Saturday, 6=Sunday
    df['daytype'] = df['Date'].map(lambda x: 'weekday' if pd.to_datetime(x).weekday() < 5 else 'weekend')
    
    # 4. Rename hourly columns from 'Hr 1'...'Hr 24' to 'hr1'...'hr24'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hr {i}'] = f'hr{i}'
    df = df.rename(columns=rename_dict)
    
    # 5. Define target columns
    target_cols = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Return the dataframe with only the target columns
    return df[target_cols]