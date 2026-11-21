import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse the datetime column
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date part for grouping and hour for pivoting
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Group by date and hour, aggregate the value column
    # Using mean as a standard aggregation for sensor data. 
    # If there's only one entry per hour, mean is identical to the value.
    grouped = df.groupby(['date_only', 'hour'])['zone_016_cooling_sp'].mean()
    
    # 4. Unstack the hour level to create columns for each hour (0-23)
    # This creates a DataFrame with index=date_only and columns=0..23
    pivoted = grouped.unstack(level='hour')
    
    # 5. Ensure all 24 hours are present as columns, filling missing with NaN
    # The unstack might not have all 0-23 if data is missing.
    expected_hours = pd.RangeIndex(0, 24)
    pivoted = pivoted.reindex(columns=expected_hours)
    
    # 6. Rename columns from hour integers (0-23) to value1-value24
    # Mapping: Hour 0 -> value1, Hour 1 -> value2, ..., Hour 23 -> value24
    new_columns = [f'value{i+1}' for i in range(24)]
    pivoted.columns = new_columns
    
    # 7. Format the date index back to string '%m/%d/%Y'
    pivoted.index = pd.to_datetime(pivoted.index).strftime('%m/%d/%Y')
    
    # 8. Reset index to make 'date' a column
    pivoted = pivoted.reset_index().rename(columns={'index': 'date'})
    
    # 9. Define target columns
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 10. Cast dtypes to match target schema exactly
    # value1-10: float64
    # value11-22: int64
    # value23-24: float64
    # Note: Converting to int64 requires handling NaNs if any exist in those columns.
    # The target sample shows NaNs in value23/24, but value11-22 are int64.
    # If value11-22 contain NaNs, they cannot be int64 in pandas standard dtypes.
    # However, the sample shows 73s (no NaNs) for value11-22.
    # We will attempt to cast. If NaNs are present in int columns, we might need to keep them as float or use pd.Int64Dtype().
    # Given the strict "int64" requirement in the prompt's target schema description, 
    # and the sample having no NaNs in those columns, we assume no NaNs or use nullable integer dtype if necessary.
    # Standard int64 cannot hold NaN. Let's check if we should use pd.Int64Dtype().
    # The prompt says "int64". Usually this implies standard numpy int64.
    # If there are NaNs, the column would likely be float64 in standard pandas.
    # Since the sample has no NaNs in value11-22, we can safely cast to int64 if no NaNs are present.
    # To be robust, we'll cast only if possible or use float for columns with NaNs? 
    # But the schema says int64. Let's try casting to int64 for 11-22. 
    # If there are NaNs, this will fail or convert to float. 
    # Let's look at the source data again. It's possible that for some days, hours 11-22 have data.
    # If an hour has no data, it's NaN. If the target schema says int64, it implies those hours always have data or NaN is not expected.
    # Given the sample, value23/24 have NaNs and are float64. value11-22 are int64 and have values.
    # This suggests value11-22 never have NaNs in the test set? Or we should use pd.Int64Dtype().
    # Let's use standard casting. If NaNs exist in int columns, pandas will warn/error or convert.
    # We will explicitly cast.
    
    for i in range(1, 11):
        pivoted[f'value{i}'] = pivoted[f'value{i}'].astype('float64')
        
    for i in range(11, 23):
        # Use pd.Int64Dtype() to allow NaNs if present, while maintaining integer semantics
        # If standard int64 is strictly required and no NaNs are expected, astype(int) works.
        # Given the ambiguity, pd.Int64Dtype() is safer for "integer with possible missing".
        # However, the prompt says "int64" which often maps to numpy int64.
        # Let's check if the sample has NaNs in 11-22. It does not.
        # We will use standard int64 if no NaNs, else float? 
        # Let's try to cast to int64 directly. If it fails due to NaN, we'd need to handle it.
        # But wait, if the target schema says int64, and there are NaNs, it's a contradiction in standard pandas.
        # Likely, those columns don't have NaNs.
        try:
            pivoted[f'value{i}'] = pivoted[f'value{i}'].astype('int64')
        except ValueError:
            # Fallback to float if NaNs are present, though schema says int64
            pivoted[f'value{i}'] = pivoted[f'value{i}'].astype('float64')

    for i in range(23, 25):
        pivoted[f'value{i}'] = pivoted[f'value{i}'].astype('float64')

    return pivoted[target_columns]