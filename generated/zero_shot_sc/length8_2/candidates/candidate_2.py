import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Parse the 'date' column into datetime objects.
    2. Extract 'Hour' and 'Month' components.
    3. Map month numbers to month names.
    4. Group by 'Hour' and 'Month', aggregating 'zone_016' using median.
    5. Pivot/Unstack to get Months as columns.
    6. Ensure all 12 month columns are present.
    7. Reindex Hours to 0-23 to ensure 24 rows.
    8. Return the formatted DataFrame.
    """
    # 1. Parse date
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract components
    df['Hour'] = df['date'].dt.hour
    df['Month'] = df['date'].dt.month
    
    # 3. Map months to names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['Month_Name'] = df['Month'].map(month_map)
    
    # 4. Aggregate
    # Using median to handle potential outliers and match the sample behavior
    # where 67.9 (majority) was chosen over 69 (minority).
    agg_df = df.groupby(['Hour', 'Month_Name'])['zone_016'].median()
    
    # 5. Unstack to create columns for months
    # agg_df is a Series with MultiIndex (Hour, Month_Name)
    # We unstack the Month_Name level
    pivot_df = agg_df.unstack(fill_value=np.nan)
    
    # 6. Ensure all 12 month columns exist
    target_months = ['January', 'February', 'March', 'April', 'May', 'June', 
                     'July', 'August', 'September', 'October', 'November', 'December']
    
    # Reindex columns to ensure order and presence
    pivot_df = pivot_df.reindex(columns=target_months)
    
    # 7. Ensure all 24 hours (0-23) are present as rows
    # The problem states Target rows: 24. This implies a full day cycle.
    all_hours = range(24)
    pivot_df = pivot_df.reindex(index=all_hours)
    
    # 8. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'index': 'Hour'}, inplace=True)
    
    # Ensure Hour is int
    pivot_df['Hour'] = pivot_df['Hour'].astype(int)
    
    # 9. Select and order final columns
    target_columns = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
    
    return pivot_df[target_columns]