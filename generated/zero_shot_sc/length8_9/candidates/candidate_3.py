import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing hourly energy rates into a summary
    DataFrame with hours as rows and months as columns, containing the sum of
    rates for each hour across all days in that month.
    """
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse the Date column
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Extract the month name in lowercase to match target column headers
    df['month'] = df['Date'].dt.strftime('%B').str.lower()
    
    # 3. Identify the hour columns (Hr 1 to Hr 24)
    hour_cols = [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Melt the DataFrame from wide to long format
    # id_vars keeps 'month' as an identifier
    # value_vars are the hour columns
    # var_name will be the column containing 'Hr 1', 'Hr 2', etc.
    # value_name will be the actual numeric values
    df_melted = df.melt(
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_label', 
        value_name='value'
    )
    
    # 5. Extract the integer hour from the hour_label (e.g., 'Hr 1' -> 1)
    df_melted['hour'] = df_melted['hour_label'].apply(lambda x: int(x.split(' ')[1]))
    
    # 6. Aggregate the data: Sum the values for each hour and month combination
    # This sums across all companies, rates, and days within that month
    df_agg = df_melted.groupby(['hour', 'month'])['value'].sum().reset_index()
    
    # 7. Pivot the data to get months as columns and hours as rows
    df_pivot = df_agg.pivot(index='hour', columns='month', values='value').reset_index()
    
    # 8. Define the target month columns in chronological order
    target_months = [
        'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Ensure all target month columns exist (in case a month is missing in data)
    for month in target_months:
        if month not in df_pivot.columns:
            df_pivot[month] = 0.0
            
    # 9. Construct the final list of columns
    target_columns = ['hour'] + target_months
    
    # 10. Select and order the columns
    df_result = df_pivot[target_columns]
    
    # 11. Ensure 'hour' is integer type
    df_result['hour'] = df_result['hour'].astype(int)
    
    # 12. Sort by hour to ensure 1-24 order
    df_result = df_result.sort_values('hour').reset_index(drop=True)
    
    return df_result