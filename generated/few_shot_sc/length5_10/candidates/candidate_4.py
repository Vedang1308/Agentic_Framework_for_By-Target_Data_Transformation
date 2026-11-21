import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Rename the Date column to date
    # The format '%a %m/%d/%Y' is identical in source and target, so we can just rename.
    df = df.rename(columns={'Date': 'date'})
    
    # 2. Map hourly columns to value columns
    # Source: '1:00'...'23:00', '24:00:00'
    # Target: 'value1'...'value24'
    rename_dict = {}
    
    # Map hours 1 to 23
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'value{i}'
        
    # Map hour 24 (source has '24:00:00')
    rename_dict['24:00:00'] = 'value24'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Drop the Segment column as it is not in the target
    if 'Segment' in df.columns:
        df = df.drop(columns=['Segment'])
        
    # 4. Define target columns in the exact order required
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 5. Return the dataframe with only the target columns
    return df[target_columns]