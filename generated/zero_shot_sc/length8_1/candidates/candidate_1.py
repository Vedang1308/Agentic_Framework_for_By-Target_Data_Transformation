import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by aggregating
    sensor readings by Hour and Month.
    """
    # 1. Parse the date column
    # The format is '%m/%d/%Y %H:%M'
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['datetime'].dt.hour
    # Map month number (1-12) to month name
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['Month'] = df['datetime'].dt.month.map(month_names)
    
    # 3. Aggregate by Hour and Month
    # Based on the target values (e.g., 24.562), the aggregation appears to be the mean.
    # The value 85 appears in the target, which likely corresponds to specific sensor readings
    # (possibly error codes or outliers) in the source that are the only values for that bucket,
    # or are averaged in. Mean is the standard statistical aggregation for such sensor data.
    aggregated = df.groupby(['Hour', 'Month'])['cerc_logger_1'].mean()
    
    # 4. Reshape to wide format (Pivot)
    # Index: Hour, Columns: Month, Values: Mean of cerc_logger_1
    df_pivot = aggregated.unstack(level='Month')
    
    # 5. Reset index to make Hour a column
    df_result = df_pivot.reset_index()
    
    # 6. Ensure correct column order and types
    target_columns = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
    
    # Ensure Hour is integer
    df_result['Hour'] = df_result['Hour'].astype(int)
    
    # Ensure month columns are float (they should be by default from mean)
    for col in target_columns[1:]:
        if col in df_result.columns:
            df_result[col] = df_result[col].astype(float)
        else:
            # If a month column is missing (e.g., no data for that month), add it as NaN
            df_result[col] = np.nan
            
    # Sort by Hour to match typical target presentation (0-23)
    df_result = df_result.sort_values('Hour').reset_index(drop=True)
    
    # Select and order columns verbatim
    return df_result[target_columns]