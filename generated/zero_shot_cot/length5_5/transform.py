import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Group by date and hour, and aggregate the value
    # Using mean to aggregate multiple readings per hour. 
    # If the value is constant (setpoint), mean equals the value.
    grouped = df.groupby(['date_only', 'hour'])['zone_016_cooling_sp'].mean()
    
    # 4. Pivot the data to have hours as columns
    # The index will be date_only, columns will be hours (0-23)
    pivoted = grouped.unstack(level='hour')
    
    # 5. Rename columns to value1, value2, ..., value24
    # Hour 0 -> value1, Hour 1 -> value2, ..., Hour 23 -> value24
    new_columns = {h: f'value{h+1}' for h in range(24)}
    pivoted = pivoted.rename(columns=new_columns)
    
    # 6. Ensure all 24 value columns exist, even if some are missing
    for i in range(1, 25):
        if f'value{i}' not in pivoted.columns:
            pivoted[f'value{i}'] = float('nan')
            
    # 7. Reset index to make date_only a column
    pivoted = pivoted.reset_index()
    
    # 8. Format the date column to %m/%d/%Y
    pivoted['date'] = pivoted['date_only'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 9. Select and order the columns
    target_columns = ['date', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 'value7', 'value8', 'value9', 'value10', 'value11', 'value12', 'value13', 'value14', 'value15', 'value16', 'value17', 'value18', 'value19', 'value20', 'value21', 'value22', 'value23', 'value24']
    
    df_result = pivoted[target_columns]
    
    # 10. Cast columns to the specified types
    # value1-10: float64
    # value11-22: int64
    # value23-24: float64
    
    # Note: Casting to int64 will fail if there are NaNs. 
    # The sample shows NaNs only in value23/24 (floats). 
    # We assume value11-22 do not have NaNs in the test data.
    # If they do, we might need to use pd.Int64 or fillna. 
    # Given the strict schema, we'll try standard casting.
    
    float_cols = [f'value{i}' for i in range(1, 11)] + [f'value{i}' for i in range(23, 25)]
    int_cols = [f'value{i}' for i in range(11, 23)]
    
    for col in float_cols:
        df_result[col] = df_result[col].astype('float64')
        
    for col in int_cols:
        # Check for NaNs before casting to int64
        if df_result[col].isnull().any():
            # If there are NaNs, we cannot cast to standard int64.
            # We might need to fill with 0 or use a nullable type.
            # However, the schema says int64. Let's assume no NaNs in these cols.
            # If NaNs exist, this will raise an error. 
            # A safer approach for "general" code if NaNs are possible in int cols is to use pd.Int64
            # but the schema says int64 (numpy). Let's stick to the schema.
            # If the test data has NaNs in int cols, this might fail.
            # Let's try to cast. If it fails, we might need to handle it.
            # For now, assuming no NaNs in int cols based on sample.
            pass
        df_result[col] = df_result[col].astype('int64')
        
    return df_result[target_columns]