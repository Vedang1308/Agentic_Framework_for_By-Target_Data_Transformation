import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by:
    1. Parsing the 'CST' date column and formatting it to 'MM/DD/YYYY'.
    2. Renaming the hourly columns from 'H:MM' format to 'Hr H' format.
    3. Reordering columns to match the target schema.
    """
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Process the Date column
    # Source format: '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # Target format: '%m/%d/%Y' (e.g., '12/01/2012')
    # We parse the datetime and then format it back to string
    df['Date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Define the column mapping for the 24 hours
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    
    col_mapping = {}
    for i in range(1, 24):
        col_mapping[f'{i}:00'] = f'Hr {i}'
    col_mapping['24:00:00'] = 'Hr 24'
    
    # Apply the rename
    df = df.rename(columns=col_mapping)
    
    # 3. Define the target column order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Select and reorder columns
    # Ensure we only select the columns that exist and are in the target order
    df = df[target_columns]
    
    # Optional: Sort by Date if the target is expected to be sorted chronologically
    # The target sample is sorted. The source sample is not.
    # To be safe and match the target sample structure, we sort by Date.
    # However, sorting might change the row order. If the row count is strictly 1-to-1,
    # sorting is a valid transformation step if the target is sorted.
    # Given the target sample is sorted, we will sort.
    df = df.sort_values(by='Date').reset_index(drop=True)
    
    return df[target_columns]