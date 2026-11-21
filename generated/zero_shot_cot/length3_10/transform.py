import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid SettingWithCopyWarning and preserve original
    df = source.copy()
    
    # 1. Transform the Date column
    # Source format: '%a %m/%d/%Y' (e.g., 'Thu 10/01/2009')
    # Target format: '%m/%d/%Y' (e.g., '01/01/2003')
    # We parse the date and then format it to the desired string representation.
    df['date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Define the mapping for hour columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hour 1', 'Hour 2', ..., 'Hour 23', 'Hour 24'
    
    # Generate source column names
    source_hour_cols = [f"{h}:00" for h in range(1, 24)] + ["24:00:00"]
    
    # Generate target column names
    target_hour_cols = [f"Hour {h}" for h in range(1, 25)]
    
    # Create a rename mapping
    rename_map = dict(zip(source_hour_cols, target_hour_cols))
    
    # Rename the columns
    df = df.rename(columns=rename_map)
    
    # 3. Select the final columns in the correct order
    target_columns = ['date'] + target_hour_cols
    
    # Ensure we only return the required columns
    df = df[target_columns]
    
    return df[target_columns]