import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Define the mapping from Time Period to season
    month_to_season = {
        'December': 'Winter', 'January': 'Winter', 'February': 'Winter',
        'March': 'Spring', 'April': 'Spring', 'May': 'Spring',
        'June': 'Summer', 'July': 'Summer', 'August': 'Summer',
        'September': 'Fall', 'October': 'Fall', 'November': 'Fall'
    }
    
    # Define the mapping from End Use to target columns
    end_use_to_target = {
        'HVAC': 'hvac',
        'Water Heating': 'water_heating',
        'Refrigerator': 'refrigerator',
        'Clothes Washer': 'clothes_washer',
        'Clothes Dryer': 'clothes_dryer',
        'Dishwasher': 'dishwasher',
        'Cooking Range': 'cooking_range',
        'Pool/Spa Pumps': 'pool_spa_pumps',
        'Interior Lighting': 'interior_lighting',
        'Exterior Lighting': 'exterior_lighting',
        'Plug': 'plug',
        'Pool/Spa Heater': 'pool_spa_heater',
        'Lighting': 'lighting'
    }
    
    # Map Time Period to season
    source['season'] = source['Time Period'].map(month_to_season)
    
    # Map End Use to target column names
    source['target_column'] = source['End Use'].map(end_use_to_target)
    
    # Filter out rows where the End Use does not map to a target column
    source = source[source['target_column'].notna()]
    
    # Fill NaN values in Average Demand Per Home With This End Use [kW] with 0
    source['Average Demand Per Home With This End Use [kW]'] = source['Average Demand Per Home With This End Use [kW]'].fillna(0)
    
    # Group by season, hour, and target_column, then sum the Average Demand Per Home With This End Use [kW]
    aggregated = source.groupby(['season', 'Hour Ending', 'target_column'])['Average Demand Per Home With This End Use [kW]'].sum().reset_index()
    
    # Pivot the data to have each target_column as a separate column
    pivoted = aggregated.pivot_table(index=['season', 'Hour Ending'], columns='target_column', values='Average Demand Per Home With This End Use [kW]', fill_value=0)
    
    # Reset index to make season and Hour Ending columns
    pivoted = pivoted.reset_index()
    
    # Rename Hour Ending to hour
    pivoted.rename(columns={'Hour Ending': 'hour'}, inplace=True)
    
    # Ensure all target columns are present and in the correct order
    target_columns = ['season', 'hour', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    
    # Add missing columns with 0 if they are not present
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = 0
    
    # Select and order the columns as per the target schema
    result = pivoted[target_columns]
    
    return result