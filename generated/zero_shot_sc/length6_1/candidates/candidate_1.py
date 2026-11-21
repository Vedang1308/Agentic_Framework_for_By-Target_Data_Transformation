import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by:
    1. Formatting the 'DT_STRATA' date column to '%m/%d/%Y' and renaming to 'Date'.
    2. Renaming 'PCT_HOURLY_XXXX' columns to 'Hr N' format.
    3. Selecting only the required columns.
    """
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Process the Date column
    # Parse the date string from source format (e.g., '7/2/2016') to datetime
    df['Date'] = pd.to_datetime(df['DT_STRATA'], format='%m/%d/%Y')
    # Format to target format (e.g., '01/01/2016') with zero-padding
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
    
    # 2. Rename the hourly columns
    # Mapping from PCT_HOURLY_XXXX to Hr N
    rename_mapping = {}
    for hour in range(1, 25):
        # Source column name format: PCT_HOURLY_0100, PCT_HOURLY_0200, ...
        src_col = f"PCT_HOURLY_{hour:04d}"
        # Target column name format: Hr 1, Hr 2, ...
        tgt_col = f"Hr {hour}"
        rename_mapping[src_col] = tgt_col
        
    df.rename(columns=rename_mapping, inplace=True)
    
    # 3. Define the target columns in the exact order required
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Select and return the final DataFrame
    return df[target_columns]