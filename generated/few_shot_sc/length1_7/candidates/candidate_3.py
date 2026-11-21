import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the 'Date' column and format it into 'cst'
    # The source format is '%a %m/%d/%Y' (e.g., 'Thu 10/01/2009')
    # We parse it to datetime to ensure consistency, then format back to string.
    dt = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename the last hour column from '24:00:00' to '24:00'
    rename_dict = {'24:00:00': '24:00'}
    df = df.rename(columns=rename_dict)
    
    # 3. Define the target columns in the correct order
    # 'cst' followed by hours 1:00 to 24:00
    target_cols = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 4. Select only the required columns (this implicitly drops 'Segment' and 'Date')
    return df[target_cols]