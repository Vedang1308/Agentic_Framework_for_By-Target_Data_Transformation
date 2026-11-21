import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column and format it to the target format '%a %m/%d/%Y'
    # Source date format is '%m/%d/%Y' (e.g., '7/3/2011')
    dt_series = pd.to_datetime(df['date'])
    df['cst'] = dt_series.dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename value columns to hour columns
    # value1 -> '1:00', ..., value24 -> '24:00'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'value{i}'] = f'{i}:00'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in the correct order
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 4. Select and return the required columns
    # This automatically drops the metadata columns (class, Description, analysis, uom)
    return df[target_columns]