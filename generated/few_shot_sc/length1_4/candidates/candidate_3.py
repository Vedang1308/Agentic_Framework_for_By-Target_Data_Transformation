import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the 'Date' column to datetime
    # The source format is '%m/%d/%Y' (e.g., '7/3/2013')
    dt = pd.to_datetime(df['Date'])
    
    # 2. Format the date for the 'cst' column
    # The target format is '%a %m/%d/%Y' (e.g., 'Tue 01/01/2013')
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 3. Rename hourly columns from '1'...'24' to '1:00'...'24:00'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[str(i)] = f"{i}:00"
    
    df = df.rename(columns=rename_dict)
    
    # 4. Define the target columns verbatim
    target_columns = ['cst'] + [f"{i}:00" for i in range(1, 25)]
    
    # 5. Return the dataframe with only the target columns
    return df[target_columns]