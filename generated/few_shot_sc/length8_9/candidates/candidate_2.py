import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the Date column
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 2. Extract month name for later use
    # Map month number to lowercase name
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df['month_name'] = df['Date'].dt.month.map(month_map)
    
    # 3. Identify hourly columns
    hour_cols = [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Melt the dataframe to long format
    # Keep 'Date', 'month_name' and other metadata if needed, but primarily we need Date and Hour Value
    # We only need to keep columns that help us identify the row's month and the hour value.
    # Company, Rate, Rate Code are not needed for the aggregation unless specified, but summing all values implies aggregating across all entities.
    df_melted = df.melt(
        id_vars=['Date', 'month_name'], 
        value_vars=hour_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # 5. Extract hour integer from 'hour_col' (e.g., 'Hr 1' -> 1)
    df_melted['hour'] = df_melted['hour_col'].str.extract(r'(\d+)').astype(int)
    
    # 6. Aggregate by hour and month_name, summing the values
    aggregated = df_melted.groupby(['hour', 'month_name'])['value'].sum().reset_index()
    
    # 7. Pivot to get months as columns
    # Index: hour, Columns: month_name, Values: value
    pivoted = aggregated.pivot(index='hour', columns='month_name', values='value')
    
    # 8. Reset index to make 'hour' a column again
    pivoted = pivoted.reset_index()
    
    # 9. Ensure column order and names match target
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # Fill any potential NaNs if a month/hour combo is missing (though unlikely with full data)
    pivoted = pivoted.fillna(0)
    
    # Select and reorder columns
    result = pivoted[target_columns]
    
    # Ensure hour is int64 and others are float64
    result['hour'] = result['hour'].astype('int64')
    for col in target_columns[1:]:
        result[col] = result[col].astype('float64')
        
    # Sort by hour to ensure correct order 1-24
    result = result.sort_values('hour').reset_index(drop=True)
    
    return result[target_columns]