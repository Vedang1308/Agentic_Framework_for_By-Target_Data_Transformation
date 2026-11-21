import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Melt the dataframe from wide to long format
    # We keep 'date' and melt 'value1'...'value24'
    # The column names 'value1'...'value24' imply hours 1 to 24
    value_cols = [f'value{i}' for i in range(1, 25)]
    
    melted = df.melt(
        id_vars=['date'],
        value_vars=value_cols,
        var_name='hour_str',
        value_name='value'
    )
    
    # 2. Extract hour number from 'hour_str' (e.g., 'value1' -> 1)
    melted['hour'] = melted['hour_str'].str.extract('(\d+)').astype(int)
    
    # 3. Parse date and extract month
    dt = pd.to_datetime(melted['date'], format='%m/%d/%Y')
    melted['month'] = dt.dt.month
    
    # 4. Group by hour and month, and calculate the mean value
    # Using mean is standard for load profiles to get an average profile
    aggregated = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 5. Pivot the table so that months become columns
    # Index: hour, Columns: month, Values: value
    pivoted = aggregated.pivot(index='hour', columns='month', values='value')
    
    # 6. Rename month columns to lowercase month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivoted.rename(columns=month_names, inplace=True)
    
    # 7. Reset index to make 'hour' a column again
    pivoted.reset_index(inplace=True)
    
    # 8. Ensure the column order matches the target schema
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Select only the target columns (handling cases where some months might be missing from data)
    # If a month is missing, it will be NaN, which is expected.
    # We need to ensure all target columns exist in the dataframe for the final selection
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = float('nan')
            
    df_result = pivoted[target_columns]
    
    # Sort by hour to ensure correct row order (1-24)
    df_result = df_result.sort_values('hour').reset_index(drop=True)
    
    # Ensure 'hour' is int64
    df_result['hour'] = df_result['hour'].astype('int64')
    
    return df_result[target_columns]