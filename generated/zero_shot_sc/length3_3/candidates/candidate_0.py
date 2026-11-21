import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms a long-format source DataFrame with datetime and value columns
    into a wide-format target DataFrame with daily rows and hourly columns.
    """
    
    # 1. Parse the datetime column
    # Source format: '%m/%d/%Y %H:%M'
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Date string for the row index (Target format: '%m/%d/%Y')
    df['date_str'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract Hour for the columns
    # Target 'Hour 1' corresponds to 00:00 (hour 0), so we add 1 to the hour index
    df['hour_num'] = df['parsed_date'].dt.hour + 1
    
    # 4. Pivot the data
    # Aggregate using 'mean' to handle multiple readings per hour.
    # If only one reading exists, mean returns that value.
    # If all are NaN, mean returns NaN.
    pivot_df = df.pivot_table(
        index='date_str', 
        columns='hour_num', 
        values='zone_016', 
        aggfunc='mean'
    )
    
    # 5. Rename columns to match target verbatim: 'Hour 1', 'Hour 2', ... 'Hour 24'
    pivot_df.columns = [f"Hour {col}" for col in pivot_df.columns]
    
    # 6. Reset index to make 'date_str' a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Rename the index column to 'date'
    pivot_df = pivot_df.rename(columns={'date_str': 'date'})
    
    # 8. Define the exact target column order
    target_columns = ['date'] + [f"Hour {i}" for i in range(1, 25)]
    
    # 9. Ensure all target columns exist (fill missing hours with NaN if necessary)
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 10. Select and order the columns as required
    result_df = pivot_df[target_columns]
    
    # 11. Ensure numeric columns are float64 as per target schema
    for col in target_columns[1:]:
        result_df[col] = result_df[col].astype(float)
        
    return result_df