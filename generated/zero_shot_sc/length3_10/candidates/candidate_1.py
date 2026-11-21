import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the source Date column and format it to match target 'date'
    # Source format: '%a %m/%d/%Y' (e.g., 'Thu 10/01/2009')
    # Target format: '%m/%d/%Y' (e.g., '01/01/2003')
    df['date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Rename the hourly columns from 'H:00' or '24:00:00' to 'Hour H'
    rename_dict = {}
    for h in range(1, 24):
        rename_dict[f"{h}:00"] = f"Hour {h}"
    rename_dict["24:00:00"] = "Hour 24"
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define the target columns in the correct order
    target_columns = ['date'] + [f'Hour {h}' for h in range(1, 25)]
    
    # 4. Select only the required columns. 
    # We drop 'Segment' and 'Date' implicitly by selection.
    df = df[target_columns]
    
    return df[target_columns]