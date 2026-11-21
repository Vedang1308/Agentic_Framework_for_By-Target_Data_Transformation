import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Parse the 'date' column into datetime objects.
    2. Extract the date part and the hour part.
    3. Map the hour (0-23) to the target column labels ('1:00'-'24:00').
       Mapping: Hour H -> Label str(H+1) + ':00'
    4. Group by Date and Hour Label, and sum the 'cerc_logger_1' values.
    5. Pivot the data to have Dates as rows and Hour Labels as columns.
    6. Format the Date index as '%a %m/%d/%Y' and rename to 'cst'.
    7. Fill missing values with 0.
    8. Ensure all target columns exist and are in the correct order.
    """
    
    # 1. Parse date
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hour to target column label
    # Hour 0 -> '1:00', Hour 1 -> '2:00', ..., Hour 23 -> '24:00'
    df['hour_label'] = df['hour'].apply(lambda h: f"{h+1}:00")
    
    # 4. Aggregate by Date and Hour Label
    # We sum the values. Based on sample analysis, sum fits the magnitude.
    agg_df = df.groupby(['date_only', 'hour_label'])['cerc_logger_1'].sum().reset_index()
    
    # 5. Pivot
    # Rows: date_only, Columns: hour_label, Values: cerc_logger_1
    pivot_df = agg_df.pivot(index='date_only', columns='hour_label', values='cerc_logger_1')
    
    # 6. Format date column
    # Convert index to datetime to format, then to string
    pivot_df.index = pd.to_datetime(pivot_df.index)
    pivot_df.index = pivot_df.index.strftime('%a %m/%d/%Y')
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'index': 'cst'}, inplace=True)
    
    # 7. Fill missing values with 0
    pivot_df = pivot_df.fillna(0)
    
    # 8. Define target columns and ensure order
    target_columns = ['cst', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', 
                      '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', 
                      '19:00', '20:00', '21:00', '22:00', '23:00', '24:00']
    
    # Ensure all target columns exist, filling with 0 if a column is missing for some rows
    for col in target_columns[1:]: # Skip 'cst'
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # Select and order columns
    result_df = pivot_df[target_columns]
    
    # Sort by date? The target sample seems sorted by date descending or ascending?
    # Sample: Sat 07/20/2019, Sun 05/13/2018... It looks like it might be sorted by date.
    # Let's convert cst back to datetime for sorting to be safe, then format again?
    # Or just sort by the string if the format allows lexicographical sort? 
    # '%a %m/%d/%Y' does not sort correctly lexicographically (e.g., Mon vs Tue).
    # However, the problem doesn't explicitly state sort order, but usually, it's good practice.
    # Let's look at the sample: 
    # Sat 07/20/2019
    # Sun 05/13/2018
    # Sat 11/24/2018
    # Thu 05/10/2018
    # This is NOT sorted by date. It might be sorted by the original appearance or random.
    # Given the instruction "generalize to any unseen test table", and no explicit sort instruction,
    # we will leave the order as determined by the groupby/pivot (which is usually sorted by index).
    # Pandas groupby sorts by default. So dates will be sorted ascending.
    
    return result_df