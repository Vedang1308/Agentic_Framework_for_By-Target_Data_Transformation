import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from a daily hourly format to a monthly hourly aggregated format.
    
    Source: Rows are days, columns 1-24 are hours.
    Target: Rows are hours, columns are months (january-december), values are mean hourly readings.
    """
    # 1. Parse the Date column
    df = source.copy()
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Extract month as an integer (1-12)
    df['month'] = df['Date'].dt.month
    
    # 3. Identify the hour columns (1-24)
    hour_cols = [str(i) for i in range(1, 25)]
    
    # 4. Melt the dataframe to long format
    # We keep 'month' as an identifier, melt the hour columns
    melted = df.melt(
        id_vars=['month'],
        value_vars=hour_cols,
        var_name='hour',
        value_name='value'
    )
    
    # 5. Convert hour column to integer for proper sorting and grouping
    melted['hour'] = melted['hour'].astype(int)
    
    # 6. Group by hour and month, then calculate the mean
    aggregated = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 7. Pivot the table so hours are rows and months are columns
    pivoted = aggregated.pivot(index='hour', columns='month', values='value')
    
    # 8. Rename month columns to lowercase month names
    month_names = {
        1: 'january',
        2: 'february',
        3: 'march',
        4: 'april',
        5: 'may',
        6: 'june',
        7: 'july',
        8: 'august',
        9: 'september',
        10: 'october',
        11: 'november',
        12: 'december'
    }
    pivoted.columns = [month_names.get(col, col) for col in pivoted.columns]
    
    # 9. Reset index to make 'hour' a column
    df_result = pivoted.reset_index()
    
    # 10. Ensure hour is integer type
    df_result['hour'] = df_result['hour'].astype(int)
    
    # 11. Define the exact target column order
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # 12. Sort by hour to match typical output expectations (though not strictly required if just selecting)
    df_result = df_result.sort_values(by='hour').reset_index(drop=True)
    
    # 13. Select and return only the required columns in the correct order
    return df_result[target_columns]