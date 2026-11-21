import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with daily hourly data into the target format.
    
    Steps:
    1. Parse the 'CST' column to extract the date in 'MM/DD/YYYY' format.
    2. Rename the hourly columns from 'H:00' format to 'Hr H' format.
    3. Reorder columns to match the target schema.
    """
    # Create a copy to avoid SettingWithCopyWarning and modify freely
    df = source.copy()
    
    # 1. Parse and format the Date column
    # Source format: 'Sat 12/01/2012' -> '%a %m/%d/%Y'
    # Target format: '12/01/2012' -> '%m/%d/%Y'
    df['Date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Define the column mapping for hours
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    
    # Generate the list of source hour columns
    # Hours 1-23 are 'H:00', Hour 24 is '24:00:00'
    source_hour_cols = [f"{h}:00" for h in range(1, 24)] + ["24:00:00"]
    
    # Generate the list of target hour columns
    target_hour_cols = [f"Hr {h}" for h in range(1, 25)]
    
    # Create the mapping dictionary
    rename_map = dict(zip(source_hour_cols, target_hour_cols))
    
    # Rename the columns
    df.rename(columns=rename_map, inplace=True)
    
    # 3. Drop the original CST column
    df.drop(columns=['CST'], inplace=True)
    
    # 4. Define the final column order
    target_columns = ['Date'] + target_hour_cols
    
    # 5. Select and return the columns in the correct order
    # Ensure all target columns exist (they should based on the schema)
    return df[target_columns]