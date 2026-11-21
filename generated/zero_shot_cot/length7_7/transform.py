import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse the date column
    # The format is '%m/%d/%Y'
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Extract 'month' as full name (e.g., 'January')
    df['month'] = df['parsed_date'].dt.strftime('%B')
    
    # 3. Extract 'daytype'
    # dayofweek: 0=Monday, ..., 4=Friday, 5=Saturday, 6=Sunday
    # Weekday: 0-4, Weekend: 5-6
    df['daytype'] = df['parsed_date'].dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # 4. Rename hour columns from 'Hour X' to 'hrX'
    rename_map = {}
    for i in range(1, 25):
        rename_map[f'Hour {i}'] = f'hr{i}'
    
    df.rename(columns=rename_map, inplace=True)
    
    # 5. Define the target columns in the correct order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Select and return the final dataframe
    # Note: We drop the helper columns 'date' and 'parsed_date' implicitly by selection
    return df[target_columns]