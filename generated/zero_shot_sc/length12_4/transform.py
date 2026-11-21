import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Step 1: Map Time Period to season
    month_to_season = {
        'December': 'Winter', 'January': 'Winter', 'February': 'Winter',
        'March': 'Spring', 'April': 'Spring', 'May': 'Spring',
        'June': 'Summer', 'July': 'Summer', 'August': 'Summer',
        'September': 'Fall', 'October': 'Fall', 'November': 'Fall'
    }
    df = source.copy()
    df['season'] = df['Time Period'].map(month_to_season)
    
    # Step 2: Map End Use to target column names
    end_use_to_col = {
        'HVAC': 'hvac',
        'Water Heater': 'water_heating',
        'Refrigerator': 'refrigerator',
        'Freezer': 'refrigerator',
        'Clothes Washer': 'clothes_washer',
        'Clothes Dryer': 'clothes_dryer',
        'Dishwasher': 'dishwasher',
        'Cooking Range': 'cooking_range',
        'Oven': 'cooking_range',
        'Microwave': 'cooking_range',
        'Pool/Spa Pumps': 'pool_spa_pumps',
        'Interior Lighting': 'interior_lighting',
        'Exterior Lighting': 'exterior_lighting',
        'Lighting': 'lighting',
        'Plug Loads': 'plug',
        'Miscellaneous': 'plug',
        'Pool/Spa Heater': 'pool_spa_heater'
    }
    
    df['target_col'] = df['End Use'].map(end_use_to_col)
    
    # Step 3: Filter out rows where target_col is NaN (i.e., not in our mapping)
    df = df.dropna(subset=['target_col'])
    
    # Step 4: Pivot the table
    # We want to group by season and hour, and sum the average demand for each target column
    pivot_df = df.pivot_table(
        index=['season', 'Hour Ending'],
        columns='target_col',
        values='Average Demand Per Home With This End Use [kW]',
        aggfunc='sum',
        fill_value=0
    )
    
    # Step 5: Reset index and rename columns
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'Hour Ending': 'hour'}, inplace=True)
    
    # Step 6: Ensure all target columns are present, even if empty
    target_columns = [
        'season', 'hour', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer',
        'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps',
        'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater'
    ]
    
    # Ensure all columns exist
    for col in target_columns[2:]:  # Skip 'season' and 'hour'
        if col not in pivot_df.columns:
            pivot_df[col] = 0
    
    # Step 7: Select and order columns
    result = pivot_df[target_columns]
    
    # Step 8: Convert hour to int64
    result['hour'] = result['hour'].astype('int64')
    
    # Step 9: Ensure numeric columns are float64 or int64 as per target schema
    # From target schema: hvac, water_heating, refrigerator, dishwasher are float64
    # Others are int64
    float_cols = ['hvac', 'water_heating', 'refrigerator', 'dishwasher']
    int_cols = ['clothes_washer', 'clothes_dryer', 'cooking_range', 'pool_spa_pumps',
                'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    
    for col in float_cols:
        result[col] = result[col].astype('float64')
    for col in int_cols:
        result[col] = result[col].astype('int64')
    
    return result