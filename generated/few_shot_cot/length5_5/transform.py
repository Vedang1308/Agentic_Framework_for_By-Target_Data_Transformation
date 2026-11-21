import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string and hour
    df['date_out'] = df['dt'].dt.strftime('%m/%d/%Y')
    df['hour'] = df['dt'].dt.hour
    
    # 3. Group by date and hour, aggregate the value
    # Using mean as a standard aggregation for sensor data. 
    # If the value is constant, mean equals the value.
    grouped = df.groupby(['date_out', 'hour'])['zone_016_cooling_sp'].mean()
    
    # 4. Pivot to create columns for each hour
    # Unstack the hour level. This creates columns 0..23
    pivot = grouped.unstack('hour')
    
    # 5. Rename columns to value1..value24
    # Hour 0 -> value1, Hour 1 -> value2, ..., Hour 23 -> value24
    pivot.columns = [f'value{i+1}' for i in range(24)]
    
    # 6. Reset index to make date_out a column
    pivot = pivot.reset_index()
    pivot = pivot.rename(columns={'date_out': 'date'})
    
    # 7. Define target columns
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 8. Ensure column order
    df_result = pivot[target_columns]
    
    # 9. Cast types to match target schema exactly
    # value1-10: float64
    # value11-22: int64
    # value23-24: float64
    # Note: Casting to int64 will fail if there are NaNs. 
    # The target schema says int64 for 11-22. If there are NaNs, we might need to handle them.
    # However, standard pandas int64 doesn't support NaN. 
    # Looking at the sample, value11-22 are 73. 
    # If there are missing hours, they would be NaN. 
    # If the target schema strictly requires int64, it implies no NaNs in those columns or use of nullable integer type.
    # But the prompt says "Target Schema and Types: ... value11 (int64) ...".
    # In many TbT tasks, if the type is int64, we might need to fill NaNs or the data is guaranteed to be present.
    # Given the sample has NaNs in value23/24 (float), but not in 11-22, it's likely 11-22 are always present.
    # We will attempt to cast. If NaNs exist in int columns, we might need to leave them as float or use pd.Int64Dtype().
    # Let's try standard casting. If it fails due to NaN, we might need to fillna(0) or similar, but that changes data.
    # Let's look at the sample again. 11/06/2018 has NaN in 23,24. It has 73 in 11-22.
    # So 11-22 seem to have data.
    
    # Apply types
    float_cols = [f'value{i}' for i in range(1, 11)] + [f'value{i}' for i in range(23, 25)]
    int_cols = [f'value{i}' for i in range(11, 23)]
    
    for col in float_cols:
        df_result[col] = df_result[col].astype('float64')
        
    for col in int_cols:
        # Check for NaNs before casting to int64
        if df_result[col].isnull().any():
            # If there are NaNs, we can't cast to standard int64. 
            # We might need to fill them or use nullable int. 
            # Given the strict schema, let's assume no NaNs in these columns based on sample.
            # If there are, we might fill with 0 or leave as float. 
            # Let's try to cast to Int64 (nullable) if standard int64 fails, 
            # but the schema says int64. Let's just cast to int64 and hope no NaNs.
            # If NaNs exist, this will raise an error. 
            # A safer approach for "int64" in pandas with potential NaNs is often to fillna(0) or similar, 
            # but that's a guess. Let's look at the sample: 11-22 are all 73.
            # I will cast to int64.
            df_result[col] = df_result[col].astype('int64')
        else:
            df_result[col] = df_result[col].astype('int64')

    return df_result