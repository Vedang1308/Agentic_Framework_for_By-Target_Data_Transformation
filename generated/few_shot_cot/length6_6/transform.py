import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column and format it to the target format
    # Source format: '%m/%d/%Y' (e.g., '7/3/2015')
    # Target format: '%Y-%m-%d %H:%M:%S' (e.g., '2015-01-01 00:00:00')
    dt = pd.to_datetime(df['date'])
    df['Date'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename the hour columns from 'Hour X' to 'Hr X'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hour {i}'] = f'Hr {i}'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define the target columns in the exact order required
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Return the dataframe with only the target columns
    return df[target_columns]