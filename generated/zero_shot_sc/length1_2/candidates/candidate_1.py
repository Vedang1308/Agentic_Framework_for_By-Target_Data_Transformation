import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse the date column
    # The source format is '%m/%d/%Y'
    df['date_dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Create the 'cst' column
    # The target format is '%a %m/%d/%Y' (e.g., 'Sat 01/01/2011')
    # Note: %a gives the abbreviated weekday name (locale-dependent, but standard in pandas)
    df['cst'] = df['date_dt'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Rename value columns to time columns
    # Mapping value1 -> 1:00, value2 -> 2:00, ..., value24 -> 24:00
    rename_map = {}
    for i in range(1, 25):
        rename_map[f'value{i}'] = f'{i}:00'
    
    df.rename(columns=rename_map, inplace=True)
    
    # 4. Define the target columns in the correct order
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 5. Select only the required columns
    df = df[target_columns]
    
    # 6. Sort by the date to ensure chronological order as seen in target sample
    # We sort by the original date_dt to handle year boundaries correctly, 
    # then drop the helper column if it was kept, but we didn't keep it in selection.
    # We need to sort the dataframe. Let's use the 'cst' string? 
    # Sorting by string 'Sat 01/01/2011' might not be chronological if years differ.
    # Better to sort by the parsed date before dropping it, or re-parse.
    # Since we dropped 'date_dt' from the selection, let's re-parse 'cst' for sorting 
    # or just sort by the index if we assume input order is irrelevant and output must be sorted.
    # Let's parse 'cst' back to datetime for sorting.
    # Format: '%a %m/%d/%Y'
    # This is slightly tricky to parse directly because %a is locale specific.
    # Instead, let's keep 'date_dt' for sorting and drop it at the end.
    
    # Re-approach for sorting:
    df['date_dt'] = pd.to_datetime(df['cst'].str.split(' ').str[1:], format='%m/%d/%Y') # This is fragile
    
    # Better approach: Sort before dropping columns
    # Let's restart the selection step to include sorting
    
    # Re-creating df for clarity in sorting logic
    df['date_dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    df['cst'] = df['date_dt'].dt.strftime('%a %m/%d/%Y')
    
    # Rename columns
    df.rename(columns=rename_map, inplace=True)
    
    # Select columns including helper
    cols_to_keep = ['cst', 'date_dt'] + [f'{i}:00' for i in range(1, 25)]
    df = df[cols_to_keep]
    
    # Sort by date_dt
    df = df.sort_values(by='date_dt').reset_index(drop=True)
    
    # Drop the helper column
    df = df.drop(columns=['date_dt'])
    
    # Ensure final column order matches target exactly
    df = df[target_columns]
    
    return df[target_columns]