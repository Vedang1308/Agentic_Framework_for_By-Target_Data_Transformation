import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Parse the 'date' column into datetime objects.
    2. Extract 'Hour' and 'Month' from the datetime.
    3. Map month numbers to month names.
    4. Pivot the data to have Hours as rows and Months as columns.
    5. Aggregate values using mean.
    6. Ensure all 12 month columns are present.
    7. Format and return the result.
    """
    # 1. Parse date
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['date'].dt.hour
    df['Month'] = df['date'].dt.month
    
    # 3. Map Month numbers to names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['Month_Name'] = df['Month'].map(month_map)
    
    # 4. Pivot Table
    # We group by Hour and Month_Name, and aggregate zone_016 using mean
    pivot_df = df.pivot_table(
        index='Hour',
        columns='Month_Name',
        values='zone_016',
        aggfunc='mean'
    )
    
    # 5. Ensure all month columns exist
    target_months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Reindex columns to ensure all months are present, filling missing with NaN
    pivot_df = pivot_df.reindex(columns=target_months)
    
    # 6. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Ensure Hour is integer
    pivot_df['Hour'] = pivot_df['Hour'].astype(int)
    
    # 8. Sort by Hour to match typical target order (0-23)
    pivot_df = pivot_df.sort_values('Hour').reset_index(drop=True)
    
    # 9. Define final target columns
    target_columns = ['Hour'] + target_months
    
    # 10. Return the DataFrame with exact column names
    return pivot_df[target_columns]