import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from long format (timestamped readings) 
    to wide format (daily readings with hourly columns).
    
    Source Schema:
    - date (object): '%m/%d/%Y %H:%M'
    - zone_016_cooling_sp (float64)
    
    Target Schema:
    - Date (object): '%m/%d/%Y'
    - Hr 1 ... Hr 24 (float64)
    """
    
    # 1. Parse the date column
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract the date string for grouping and the hour for pivoting
    # Format date as MM/DD/YYYY
    df['Date'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    # Extract hour (0-23) and add 1 to make it 1-24 to match target 'Hr 1'...'Hr 24'
    df['Hour'] = df['parsed_date'].dt.hour + 1
    
    # 3. Pivot the table
    # Index: Date
    # Columns: Hour (1-24)
    # Values: zone_016_cooling_sp
    # Aggfunc: mean (handles multiple 5-min intervals per hour)
    pivot_df = df.pivot_table(
        index='Date', 
        columns='Hour', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 4. Rename columns to 'Hr 1', 'Hr 2', ..., 'Hr 24'
    # The columns are currently integers 1-24 (or subset)
    pivot_df.columns = [f'Hr {h}' for h in pivot_df.columns]
    
    # 5. Ensure all hours 1-24 are present in the columns, filling missing with NaN
    expected_hours = [f'Hr {h}' for h in range(1, 25)]
    pivot_df = pivot_df.reindex(columns=expected_hours)
    
    # 6. Reset index to make 'Date' a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Define target columns in the correct order
    target_columns = ['Date'] + [f'Hr {h}' for h in range(1, 25)]
    
    # 8. Return the DataFrame with the exact target columns
    return pivot_df[target_columns]