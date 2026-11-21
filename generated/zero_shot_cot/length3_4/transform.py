import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    # Target hours are 1-24, corresponding to 0-23 in 24-hour clock
    df['date_only'] = df['datetime'].dt.date
    df['hour_idx'] = df['datetime'].dt.hour + 1
    
    # 3. Pivot the data
    # We group by date_only and hour_idx, aggregating the cooling_sp value.
    # Using 'mean' to handle multiple entries per hour, though 'first' might also work if data is constant.
    # Given the sample output has NaNs, we need to ensure missing hours are represented as NaN.
    pivot_df = df.pivot_table(
        index='date_only', 
        columns='hour_idx', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 4. Ensure all 24 hour columns exist
    # Create a list of expected hour indices
    expected_hours = list(range(1, 25))
    
    # Reindex columns to ensure all 1-24 are present, filling missing with NaN
    pivot_df = pivot_df.reindex(columns=expected_hours, fill_value=np.nan)
    
    # 5. Rename columns to "Hour 1", "Hour 2", etc.
    pivot_df.columns = [f'Hour {h}' for h in pivot_df.columns]
    
    # 6. Reset index to make 'date_only' a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Format the date column to '%m/%d/%Y'
    pivot_df['date'] = pivot_df['date_only'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 8. Select and order columns as per target schema
    target_columns = ['date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24']
    
    # Drop the helper column if it still exists (it shouldn't after reset_index if we renamed, but date_only is the index name)
    if 'date_only' in pivot_df.columns:
        pivot_df = pivot_df.drop(columns=['date_only'])
        
    # Ensure the final dataframe has the exact columns in the correct order
    result_df = pivot_df[target_columns]
    
    return result_df