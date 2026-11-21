import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by pivoting 
    hourly sensor data into a monthly summary table.
    """
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month components
    df['Hour'] = df['datetime'].dt.hour
    df['Month'] = df['datetime'].dt.month
    
    # 3. Map Month numbers to Names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['Month_Name'] = df['Month'].map(month_map)
    
    # 4. Handle the "85" missing value flag
    # We assume 85 represents missing/invalid data.
    # We replace 85 with NaN for calculation purposes.
    df['value_clean'] = df['cerc_logger_1'].replace(85, np.nan)
    
    # 5. Aggregate: Calculate mean for each Hour and Month_Name
    # Using skipna=True is default, so NaNs (former 85s) are ignored in the mean
    aggregated = df.groupby(['Hour', 'Month_Name'])['value_clean'].mean().reset_index()
    
    # 6. Pivot the data
    # Index: Hour, Columns: Month_Name, Values: value_clean
    pivoted = aggregated.pivot(index='Hour', columns='Month_Name', values='value_clean')
    
    # 7. Reset index to make Hour a column
    pivoted = pivoted.reset_index()
    
    # 8. Handle groups that had NO valid data (all were 85 or missing)
    # These will be NaN in the pivoted table. We fill them with 85 to match target.
    pivoted = pivoted.fillna(85)
    
    # 9. Define target columns
    target_columns = [
        'Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # 10. Ensure all target columns exist (in case some months have no data at all)
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = 85 # Default to 85 if month is completely missing
            
    # 11. Sort by Hour
    pivoted = pivoted.sort_values('Hour')
    
    # 12. Select and order columns exactly as required
    result = pivoted[target_columns]
    
    # 13. Ensure correct data types
    result['Hour'] = result['Hour'].astype('int64')
    for col in target_columns[1:]:
        result[col] = result[col].astype('float64')
        
    return result