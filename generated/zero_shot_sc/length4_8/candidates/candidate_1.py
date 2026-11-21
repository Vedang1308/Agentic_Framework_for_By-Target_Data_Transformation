import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour components
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map 24-hour clock to 12-hour AM/PM labels
    # 0 -> 12:00 AM
    # 1 -> 1:00 AM
    # ...
    # 11 -> 11:00 AM
    # 12 -> 12:00 PM
    # 13 -> 1:00 PM
    # ...
    # 23 -> 11:00 PM
    
    def map_hour_to_label(h):
        if h == 0:
            return '12:00 AM'
        elif 1 <= h <= 11:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else: # 13-23
            return f'{h-12}:00 PM'
            
    df['hour_label'] = df['hour'].apply(map_hour_to_label)
    
    # 4. Aggregate by date and hour label
    # We calculate the mean of cerc_logger_1 for each date and hour
    agg_df = df.groupby(['date_only', 'hour_label'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot the table
    # Index: date_only, Columns: hour_label, Values: cerc_logger_1
    pivoted_df = agg_df.pivot(index='date_only', columns='hour_label', values='cerc_logger_1')
    
    # 6. Reset index to make date a column
    pivoted_df = pivoted_df.reset_index()
    
    # 7. Format the date column to '%m/%d/%Y'
    pivoted_df['date'] = pivoted_df['date_only'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 8. Define the target columns in the exact required order
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 9. Select and order columns
    # Note: The pivot might not have all columns if data is missing for some hours.
    # The problem statement implies a full schema. We select existing columns in order.
    # If a column is missing in the pivot, it won't be in the result unless we reindex.
    # Given the source data is dense (every 10 mins), all hours should be present.
    
    # Ensure all target columns exist (fill missing with NaN if necessary, though unlikely here)
    for col in target_columns:
        if col not in pivoted_df.columns and col != 'date':
            pivoted_df[col] = np.nan
            
    result_df = pivoted_df[target_columns]
    
    # 10. Sort by date? The target sample seems sorted by date descending or ascending?
    # Target sample: 05/08, 05/07, 03/10... It's not strictly sorted.
    # However, standard practice is often to keep the order of appearance or sort.
    # The prompt doesn't specify sorting, but usually, TbT tasks preserve group order or sort.
    # Let's check the source order. The source is not sorted.
    # The target sample shows dates: 05/08, 05/07, 03/10, 04/16, 10/08, 03/20, 07/12, 07/06.
    # This looks like it might be sorted by date descending? 
    # 05/08 > 05/07. But 03/10 < 05/07. So it's not sorted by date.
    # It might be sorted by the original appearance of the date in the source?
    # Or perhaps it's just arbitrary.
    # Usually, if not specified, we can return in any order, but matching the sample order is safer if possible.
    # However, without explicit instruction, standard aggregation often results in sorted index (ascending).
    # Let's look at the sample again.
    # 05/08/2019, 05/07/2019, 03/10/2018, 04/16/2019, 10/08/2018, 03/20/2019, 07/12/2019, 07/06/2019.
    # This order is very specific. It corresponds to the order of first appearance in the source file?
    # Or maybe it's sorted by the value of one of the columns?
    # Given the complexity of inferring row order from a small sample, and that pandas groupby/pivot 
    # typically sorts the index, let's assume the standard behavior (sorted by date) is acceptable 
    # OR we should try to preserve the order of first appearance.
    
    # Let's try to preserve the order of first appearance of the date in the source.
    # We can map the 'date' column back to the order of first appearance.
    
    # Get unique dates in order of first appearance in source
    unique_dates_order = df['date_only'].drop_duplicates().tolist()
    
    # Create a mapping for sorting
    date_order_map = {d: i for i, d in enumerate(unique_dates_order)}
    
    # Sort the result dataframe based on this order
    result_df['sort_key'] = result_df['date'].apply(lambda x: date_order_map.get(pd.Timestamp(x).date(), 9999))
    result_df = result_df.sort_values('sort_key')
    result_df = result_df.drop(columns=['sort_key'])
    
    # Reset index to be clean
    result_df = result_df.reset_index(drop=True)
    
    return result_df[target_columns]