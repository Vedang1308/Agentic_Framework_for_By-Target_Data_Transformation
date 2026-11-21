import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # Parse the date column
    df['date_dt'] = pd.to_datetime(df['date'])
    
    # Extract month name
    df['month'] = df['date_dt'].dt.strftime('%B')
    
    # Determine daytype: weekday (0-4) or weekend (5-6)
    # Monday is 0, Sunday is 6
    df['daytype'] = df['date_dt'].dt.dayofweek.apply(lambda x: 'weekend' if x >= 5 else 'weekday')
    
    # Rename value columns to hr columns
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'value{i}'] = f'hr{i}'
    df = df.rename(columns=rename_dict)
    
    # Sort by month and then by original date to match target order
    # The target sample shows grouping by month, and within month, the order seems to follow the original date sequence
    df = df.sort_values(by=['month', 'date_dt']).reset_index(drop=True)
    
    # Define target columns
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # Return the DataFrame with only the target columns
    return df[target_columns]