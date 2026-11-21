import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Make a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse the date column
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Extract month name
    df['month'] = df['date_parsed'].dt.strftime('%B')
    
    # 3. Determine daytype (weekday vs weekend)
    # Monday=0, Tuesday=1, ..., Friday=4, Saturday=5, Sunday=6
    df['daytype'] = df['date_parsed'].dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # 4. Rename value columns to hr columns
    rename_map = {f'value{i}': f'hr{i}' for i in range(1, 25)}
    df.rename(columns=rename_map, inplace=True)
    
    # 5. Define target columns
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Select only the target columns
    df = df[target_columns + ['date_parsed']]
    
    # 7. Sort by the original date to ensure chronological order (e.g., Jan before June)
    df.sort_values(by='date_parsed', inplace=True)
    
    # 8. Drop the helper date column
    df.drop(columns=['date_parsed'], inplace=True)
    
    # 9. Return the final dataframe with exact column names
    return df[target_columns]