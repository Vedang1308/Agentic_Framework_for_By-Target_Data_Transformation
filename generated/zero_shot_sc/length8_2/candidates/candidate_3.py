import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by pivoting
    hourly average values for each month.
    """
    # 1. Parse the date column
    df = source.copy()
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['date_parsed'].dt.hour
    df['Month_Num'] = df['date_parsed'].dt.month
    
    # 3. Map Month numbers to names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['Month_Name'] = df['Month_Num'].map(month_map)
    
    # 4. Aggregate: Calculate mean for each Hour and Month
    # Using 'mean' as the standard aggregation for sensor data over time.
    # dropna=True is default for mean, which handles the NaNs in the source.
    aggregated = df.groupby(['Hour', 'Month_Name'])['zone_016'].mean()
    
    # 5. Reshape: Unstack Month_Name to become columns
    # This creates a DataFrame with Hour as index and Months as columns
    pivoted = aggregated.unstack(fill_value=np.nan)
    
    # 6. Reset index to make Hour a column
    pivoted = pivoted.reset_index()
    
    # 7. Ensure all month columns are present and in correct order
    target_months = ['January', 'February', 'March', 'April', 'May', 'June', 
                     'July', 'August', 'September', 'October', 'November', 'December']
    
    # Add any missing month columns with NaN
    for month in target_months:
        if month not in pivoted.columns:
            pivoted[month] = np.nan
            
    # 8. Select and order columns
    target_columns = ['Hour'] + target_months
    
    # 9. Sort by Hour to match typical chronological order (0-23)
    pivoted = pivoted.sort_values('Hour').reset_index(drop=True)
    
    # 10. Return the final DataFrame with exact target columns
    return pivoted[target_columns]