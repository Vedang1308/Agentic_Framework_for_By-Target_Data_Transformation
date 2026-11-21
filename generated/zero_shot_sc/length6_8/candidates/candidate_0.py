import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from long format (timestamped readings) 
    to wide format (daily hourly aggregates).
    """
    # 1. Parse the date column
    # Format: '7/28/2019 4:50' -> '%m/%d/%Y %H:%M'
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %I:%M %p', errors='coerce')
    
    # If the above format fails due to 24h vs 12h ambiguity in samples, 
    # try standard mixed format. The sample '4:50' could be AM/PM. 
    # However, '23:30' in sample is clearly 24h. 
    # Let's try a more robust parsing or mixed.
    # Actually, pd.to_datetime is smart enough with mixed formats often, 
    # but explicit is better. The sample has '4:50' and '23:30'.
    # '4:50' is likely 12-hour without AM/PM specified in the string, 
    # but '23:30' is 24-hour. This is tricky.
    # Let's look at the sample again: '7/28/2019 4:50' and '12/31/2020 23:30'.
    # Standard pd.to_datetime usually handles this mix if we don't specify format strictly,
    # or we can try multiple formats.
    
    # Let's try inferring without strict format first, as it's often more robust for mixed inputs
    df['datetime'] = pd.to_datetime(df['date'], format='mixed', dayfirst=False)
    
    # 2. Extract Date and Hour
    # The target hours are 1-24. 
    # Source hour 0 (00:00-00:59) should map to Hr 1
    # Source hour 23 (23:00-23:59) should map to Hr 24
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour 0->1, 1->2, ..., 23->24
    df['target_hr_idx'] = df['hour'] + 1
    
    # 3. Aggregate
    # Group by date and target hour index, take the mean of cerc_logger_1
    # Using mean is standard for this type of sensor data reduction.
    agg_df = df.groupby(['date_only', 'target_hr_idx'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot
    # Rows: date_only, Columns: target_hr_idx, Values: cerc_logger_1
    pivot_df = agg_df.pivot(index='date_only', columns='target_hr_idx', values='cerc_logger_1')
    
    # 5. Rename Columns
    # Columns are currently 1, 2, ..., 24. Rename to 'Hr 1', 'Hr 2', ..., 'Hr 24'
    pivot_df.columns = [f'Hr {i}' for i in pivot_df.columns]
    
    # 6. Reset Index and Format Date
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'date_only': 'Date'}, inplace=True)
    
    # Format Date column to '%m/%d/%Y'
    pivot_df['Date'] = pd.to_datetime(pivot_df['Date']).dt.strftime('%m/%d/%Y')
    
    # 7. Define Target Columns
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 8. Select and Return
    # Ensure all expected columns exist (fill NaNs if any hours are missing for a day)
    # The problem implies a full 24h grid, but just in case, we can reindex columns.
    for col in target_columns[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    return pivot_df[target_columns]