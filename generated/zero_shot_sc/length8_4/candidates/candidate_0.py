import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from long format with hourly columns
    to a wide format with months as columns and hours as rows,
    aggregating by mean.
    """
    # 1. Parse the date column to extract month information
    source['DT_STRATA'] = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    source['month_num'] = source['DT_STRATA'].dt.month
    
    # 2. Identify hour columns and map them to hour integers (1-24)
    # Columns are PCT_HOURLY_0100 to PCT_HOURLY_2400
    hour_cols = [f'PCT_HOURLY_{h:04d}' for h in range(1, 25)]
    
    # 3. Melt the DataFrame to convert wide hour columns into long format
    # We keep 'month_num' as an identifier variable
    df_melted = source.melt(
        id_vars=['month_num'],
        value_vars=hour_cols,
        var_name='hour_col',
        value_name='value'
    )
    
    # 4. Extract hour number from the column name (e.g., 'PCT_HOURLY_0100' -> 1)
    df_melted['hour'] = df_melted['hour_col'].str.extract('(\d{4})').astype(int)
    
    # 5. Drop rows where value is NaN if any (though unlikely given the source structure)
    df_melted = df_melted.dropna(subset=['value'])
    
    # 6. Aggregate: Group by hour and month, calculate the mean
    df_agg = df_melted.groupby(['hour', 'month_num'])['value'].mean().reset_index()
    
    # 7. Pivot to wide format: hours as index, months as columns
    df_pivot = df_agg.pivot(index='hour', columns='month_num', values='value')
    
    # 8. Reset index to make 'hour' a column
    df_pivot = df_pivot.reset_index()
    
    # 9. Rename month columns to lowercase month names
    month_mapping = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_pivot.rename(columns=month_mapping, inplace=True)
    
    # 10. Ensure 'hour' is integer type
    df_pivot['hour'] = df_pivot['hour'].astype(int)
    
    # 11. Sort by hour to ensure correct order (1-24)
    df_pivot = df_pivot.sort_values('hour').reset_index(drop=True)
    
    # 12. Define the exact target columns
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # 13. Return the DataFrame with exactly the target columns
    return df_pivot[target_columns]