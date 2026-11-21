import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing daily hourly data into a target DataFrame
    showing the average value for each hour of each month.
    """
    # 1. Parse the Date column to extract month information
    source = source.copy()
    source['Date'] = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # 2. Melt the DataFrame to convert wide format (24 hour columns) to long format
    # We keep 'Date' and melt columns '1' through '24'
    hour_columns = [str(i) for i in range(1, 25)]
    melted_df = source.melt(
        id_vars=['Date'],
        value_vars=hour_columns,
        var_name='hour',
        value_name='value'
    )
    
    # 3. Convert hour to integer
    melted_df['hour'] = melted_df['hour'].astype(int)
    
    # 4. Extract month name from Date and convert to lowercase
    # Month 1 -> 'january', 2 -> 'february', etc.
    melted_df['month'] = melted_df['Date'].dt.month_name().str.lower()
    
    # 5. Group by hour and month, and calculate the mean value
    aggregated_df = melted_df.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 6. Pivot the table so that 'hour' is the index, 'month' are columns, and values are the means
    pivot_df = aggregated_df.pivot(index='hour', columns='month', values='value')
    
    # 7. Reset index to make 'hour' a column again
    pivot_df = pivot_df.reset_index()
    
    # 8. Define the target column order
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # 9. Ensure all target month columns exist (fill missing with NaN if necessary, though pivot usually handles this)
    for col in target_columns[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 10. Select and reorder columns to match target schema exactly
    df = pivot_df[target_columns]
    
    # 11. Sort by hour to match the logical order (though target sample isn't strictly sorted, standard practice is sorted)
    # The target sample shows hours 1, 10, 11... 6, 7... which is not sorted. 
    # However, usually "general" transformations imply a sorted or deterministic order. 
    # Let's check the target sample again. It seems somewhat random or grouped. 
    # But typically, we return sorted by the key column 'hour'.
    df = df.sort_values(by='hour').reset_index(drop=True)
    
    # Ensure hour is int64
    df['hour'] = df['hour'].astype('int64')
    
    return df[target_columns]