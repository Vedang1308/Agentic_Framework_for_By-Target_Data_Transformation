import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the Date column
    # Format is '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # 2. Create 'month' column
    # Extract full month name
    df['month'] = df['parsed_date'].dt.strftime('%B')
    
    # 3. Create 'daytype' column
    # 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    is_weekend = df['parsed_date'].dt.dayofweek.isin([5, 6])
    df['daytype'] = np.where(is_weekend, 'weekend', 'weekday')
    
    # 4. Rename hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    
    rename_map = {}
    for i in range(1, 24):
        # Columns 1 through 23 are formatted as "H:00"
        rename_map[f'{i}:00'] = f'hr{i}'
    # Column 24 is formatted as "24:00:00"
    rename_map['24:00:00'] = 'hr24'
    
    df = df.rename(columns=rename_map)
    
    # 5. Define target columns in exact order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Select and return the final DataFrame
    # Drop helper columns if any, though we only selected needed ones
    result_df = df[target_columns]
    
    return result_df