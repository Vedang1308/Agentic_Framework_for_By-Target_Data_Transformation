import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid modifying the original source
    df = source.copy()
    
    # 1. Transform the Date column
    # Source format: '%a %m/%d/%Y' (e.g., 'Thu 10/01/2009')
    # Target format: '%m/%d/%Y' (e.g., '01/01/2003')
    # Parse to datetime and then format back to string
    df['date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Define the mapping for hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hour 1', 'Hour 2', ..., 'Hour 23', 'Hour 24'
    
    # Generate source column names based on the pattern observed
    source_hour_cols = []
    for i in range(1, 24):
        source_hour_cols.append(f"{i}:00")
    source_hour_cols.append("24:00:00") # The last one is special
    
    # Generate target column names
    target_hour_cols = [f"Hour {i}" for i in range(1, 25)]
    
    # Create a rename dictionary
    rename_map = dict(zip(source_hour_cols, target_hour_cols))
    
    # Add the date rename
    rename_map['Date'] = 'date' # Although we created a new column, we can drop the old one later
    
    # 3. Rename the columns
    # We only rename the columns that exist in the map
    df = df.rename(columns=rename_map)
    
    # 4. Select the final columns in the correct order
    # The target requires 'date' followed by 'Hour 1' to 'Hour 24'
    target_columns = ['date'] + target_hour_cols
    
    # Ensure we only return the columns present in the target schema
    # Drop 'Segment' and original 'Date' implicitly by selection
    result_df = df[target_columns]
    
    return result_df