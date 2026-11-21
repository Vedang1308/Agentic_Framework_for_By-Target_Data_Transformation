import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # Parse the date column
    df['dt'] = pd.to_datetime(df['date'])
    
    # Extract date for grouping and hour for pivoting
    df['date_only'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    
    # Map hour 0 to 24, keep others as is (1-23)
    # This creates buckets 1 through 24
    df['hour_mapped'] = df['hour'].replace({0: 24})
    
    # Group by date and mapped hour, then average the values
    grouped = df.groupby(['date_only', 'hour_mapped'])['cerc_logger_1'].mean().reset_index()
    
    # Pivot the table
    pivoted = grouped.pivot(index='date_only', columns='hour_mapped', values='cerc_logger_1')
    
    # Ensure all hours 1-24 are present and fill missing with 0
    # The target has 0s for missing days/values
    for h in range(1, 25):
        if h not in pivoted.columns:
            pivoted[h] = 0
            
    # Fill any remaining NaNs with 0
    pivoted = pivoted.fillna(0)
    
    # Rename columns to match target format '1:00', '2:00', ...
    rename_dict = {h: f'{h}:00' for h in range(1, 25)}
    pivoted = pivoted.rename(columns=rename_dict)
    
    # Format the index as 'cst'
    # Convert index to datetime again for formatting if it's not already, 
    # though pivot index might be date objects.
    # pd.to_datetime handles date objects.
    pivoted.index = pd.to_datetime(pivoted.index)
    pivoted.index = pivoted.index.strftime('%a %m/%d/%Y')
    pivoted = pivoted.reset_index()
    pivoted = pivoted.rename(columns={'date_only': 'cst'})
    
    # Define target columns
    target_columns = ['cst'] + [f'{h}:00' for h in range(1, 25)]
    
    # Return the dataframe with exact target columns
    return pivoted[target_columns]