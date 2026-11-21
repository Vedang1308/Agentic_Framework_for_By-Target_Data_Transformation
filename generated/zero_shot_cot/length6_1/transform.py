import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by:
    1. Selecting the date and hourly percentage columns (excluding the 25th hour).
    2. Grouping by date and calculating the mean for each hour.
    3. Renaming columns to match the target schema.
    4. Formatting the date column.
    """
    
    # Define the target column names
    target_columns = [
        'Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 
        'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 
        'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24'
    ]
    
    # Identify source hourly columns to keep (0100 to 2400)
    hourly_cols = [f'PCT_HOURLY_{h:04d}' for h in range(1, 25)]
    
    # Select only the necessary columns: Date and the 24 hourly columns
    df_subset = source[['DT_STRATA'] + hourly_cols].copy()
    
    # Group by date and calculate the mean for each hour
    # This aggregates multiple strata rows for the same date into a single row
    df_agg = df_subset.groupby('DT_STRATA', as_index=False).mean()
    
    # Rename the date column
    df_agg.rename(columns={'DT_STRATA': 'Date'}, inplace=True)
    
    # Create a mapping for hourly columns
    rename_map = {}
    for h in range(1, 25):
        src_col = f'PCT_HOURLY_{h:04d}'
        tgt_col = f'Hr {h}'
        rename_map[src_col] = tgt_col
        
    df_agg.rename(columns=rename_map, inplace=True)
    
    # Format the Date column to ensure zero-padding (e.g., 01/01/2016)
    # Parse the date string, then format it back
    df_agg['Date'] = pd.to_datetime(df_agg['Date'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # Ensure the column order matches the target exactly
    return df_agg[target_columns]