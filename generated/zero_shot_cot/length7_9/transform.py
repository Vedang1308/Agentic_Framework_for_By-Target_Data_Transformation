import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the Date column
    # Format is '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # 2. Derive 'month' column
    # Extract full month name (e.g., 'January', 'October')
    df['month'] = df['parsed_date'].dt.month_name()
    
    # 3. Derive 'daytype' column
    # Determine if the day is a weekday or weekend
    # dayofweek: Monday=0, ..., Friday=4, Saturday=5, Sunday=6
    df['daytype'] = df['parsed_date'].dt.dayofweek.apply(
        lambda x: 'weekend' if x >= 5 else 'weekday'
    )
    
    # 4. Rename hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    
    rename_map = {}
    for h in range(1, 24):
        rename_map[f'{h}:00'] = f'hr{h}'
    rename_map['24:00:00'] = 'hr24'
    
    df = df.rename(columns=rename_map)
    
    # 5. Define target columns in the correct order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Select and return the final DataFrame
    # Ensure we only return the specified columns
    result_df = df[target_columns]
    
    return result_df