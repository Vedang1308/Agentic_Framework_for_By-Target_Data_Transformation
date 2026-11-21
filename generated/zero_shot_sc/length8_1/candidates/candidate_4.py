import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by aggregating 'cerc_logger_1' values
    by Hour and Month, then pivoting the data to have Hours as rows and
    Months as columns.
    """
    # 1. Parse the date column
    df = source.copy()
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['date_parsed'].dt.hour
    df['Month'] = df['date_parsed'].dt.month
    
    # 3. Define month name mapping
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    # 4. Aggregate by Hour and Month using Mean
    # We group by Hour and Month and calculate the mean of cerc_logger_1
    aggregated = df.groupby(['Hour', 'Month'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot the table
    # Index: Hour, Columns: Month, Values: cerc_logger_1
    pivoted = aggregated.pivot(index='Hour', columns='Month', values='cerc_logger_1')
    
    # 6. Rename columns to month names
    pivoted.rename(columns=month_map, inplace=True)
    
    # 7. Reset index to make Hour a column
    pivoted = pivoted.reset_index()
    
    # 8. Define target columns in the exact order required
    target_columns = [
        'Hour', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # 9. Ensure all target columns exist (fill NaN if a month is missing for a hour)
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = np.nan
            
    # 10. Select and order columns
    result = pivoted[target_columns]
    
    # 11. Ensure data types match target schema
    result['Hour'] = result['Hour'].astype(int)
    for month in target_columns[1:]:
        result[month] = result[month].astype(float)
        
    return result