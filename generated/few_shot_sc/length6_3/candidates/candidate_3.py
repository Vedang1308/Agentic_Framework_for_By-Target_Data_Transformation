import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format: '7/3/2011' (M/D/YYYY)
    # Target format: '2011-01-01 00:00:00' (YYYY-MM-DD HH:MM:SS)
    df['Date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d 00:00:00')
    
    # 2. Rename value columns to Hr columns
    # Map value1 -> Hr 1, ..., value24 -> Hr 24
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'value{i}'] = f'Hr {i}'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in the exact order required
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Select and return the relevant columns
    # We drop the metadata columns (class, Description, analysis, uom) implicitly by selecting only target_columns
    return df[target_columns]