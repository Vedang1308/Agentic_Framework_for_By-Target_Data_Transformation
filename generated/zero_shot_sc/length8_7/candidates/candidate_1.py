import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the Date column to extract month information
    source = source.copy()
    source['Date'] = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    source['month_num'] = source['Date'].dt.month
    
    # 2. Identify the hour columns (1 to 24)
    hour_cols = [str(i) for i in range(1, 25)]
    
    # 3. Melt the DataFrame to convert wide format to long format
    # Keep 'month_num' as an identifier, melt the hour columns into 'hour' and 'value'
    melted = source.melt(
        id_vars=['month_num'],
        value_vars=hour_cols,
        var_name='hour_str',
        value_name='value'
    )
    
    # 4. Convert hour string to integer
    melted['hour'] = melted['hour_str'].astype(int)
    
    # 5. Define month name mapping
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    melted['month_name'] = melted['month_num'].map(month_names)
    
    # 6. Aggregate (mean) by hour and month
    # We calculate the mean of 'value' for each (hour, month_name) pair
    agg_df = melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 7. Pivot the table to get months as columns and hours as index/rows
    pivot_df = agg_df.pivot_table(index='hour', columns='month_name', values='value')
    
    # 8. Reset index to make 'hour' a column
    pivot_df = pivot_df.reset_index()
    
    # 9. Ensure column names match exactly
    # The pivot columns will be the month names. We need to ensure they are present.
    # Fill NaNs if any month is missing for an hour (though mean should handle existing data)
    pivot_df = pivot_df.fillna(np.nan)
    
    # 10. Define the exact target columns
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # 11. Sort by hour to ensure deterministic order (1-24)
    pivot_df = pivot_df.sort_values('hour').reset_index(drop=True)
    
    # 12. Select and return the final DataFrame with exact column names
    # Note: Pivot table columns might not be in the exact order of target_columns if some are missing
    # We explicitly reorder.
    return pivot_df[target_columns]