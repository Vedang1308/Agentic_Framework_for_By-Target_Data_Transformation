import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame to the target schema by:
    1. Formatting the 'Date' column to 'YYYY-MM-DD HH:MM:SS' and renaming to 'date'.
    2. Renaming 'Hr 1'...'Hr 24' to 'value1'...'value24'.
    3. Dropping non-target columns ('Company', 'Rate', 'Rate Code').
    """
    df = source.copy()
    
    # 1. Parse and format the Date column
    # Source format is M/D/YYYY, Target format is YYYY-MM-DD HH:MM:SS
    df['date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename hourly columns
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hr {i}'] = f'value{i}'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 4. Select and return
    return df[target_columns]