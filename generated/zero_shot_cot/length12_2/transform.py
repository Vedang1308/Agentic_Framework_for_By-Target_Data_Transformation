import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with 15-minute interval appliance data
    into an hourly aggregated DataFrame grouped by season.
    """
    # 1. Parse the datetime column
    df = source.copy()
    df['local_15min'] = pd.to_datetime(df['local_15min'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract hour and determine season
    df['hour'] = df['local_15min'].dt.hour
    
    # Define season based on month
    # Winter: Dec (12), Jan (1), Feb (2)
    # Spring: Mar (3), Apr (4), May (5)
    # Summer: Jun (6), Jul (7), Aug (8)
    # Fall: Sep (9), Oct (10), Nov (11)
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    df['season'] = df['local_15min'].dt.month.apply(get_season)

    # 3. Define column mappings for aggregation
    # We sum the '_sum' columns for each category
    
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum'
    ]
    
    water_heating_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    refrigerator_cols = [
        'refrigerator1_sum', 'refrigerator2_sum',
        'freezer1_sum', 'icemaker1_sum', 'winecooler1_sum'
    ]
    
    clothes_washer_cols = [
        'clotheswasher1_sum', 'clotheswasher_dryg1_sum'
    ]
    
    clothes_dryer_cols = [
        'drye1_sum', 'dryg1_sum'
    ]
    
    dishwasher_cols = [
        'dishwasher1_sum'
    ]
    
    cooking_range_cols = [
        'oven1_sum', 'oven2_sum', 'range1_sum',
        'microwave1_sum', 'disposal1_sum'
    ]
    
    pool_spa_pumps_cols = [
        'poolpump1_sum', 'pump1_sum', 'jacuzzi1_sum'
    ]
    
    # Interior lighting: Sum of lighting in specific rooms
    interior_lighting_cols = [
        'bathroom1_sum', 'bathroom2_sum',
        'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
        'diningroom1_sum', 'diningroom2_sum',
        'kitchen1_sum', 'kitchen2_sum',
        'livingroom1_sum', 'livingroom2_sum',
        'office1_sum', 'utilityroom1_sum',
        'garage1_sum', 'garage2_sum', 'shed1_sum'
    ]
    
    # Exterior lighting: Outdoor lights
    exterior_lighting_cols = [
        'poollight1_sum', 'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum'
    ]
    
    # Plug loads: Miscellaneous plugs
    plug_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum',
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
        'kitchenapp1_sum', 'kitchenapp2_sum',
        'battery1_sum', 'car1_sum', 'car2_sum',
        'aquarium1_sum', 'security1_sum',
        'sumppump1_sum', 'wellpump1_sum', 'sewerpump1_sum', 'sprinkler1_sum'
    ]
    
    pool_spa_heaters_cols = [
        'pool1_sum', 'pool2_sum'
    ]

    # 4. Perform Aggregation
    # Group by season and hour, then sum the relevant columns
    grouped = df.groupby(['season', 'hour'])
    
    agg_dict = {
        'hvac': (hvac_cols, 'sum'),
        'water_heating': (water_heating_cols, 'sum'),
        'refrigerator': (refrigerator_cols, 'sum'),
        'clothes_washer': (clothes_washer_cols, 'sum'),
        'clothes_dryer': (clothes_dryer_cols, 'sum'),
        'dishwasher': (dishwasher_cols, 'sum'),
        'cooking_range': (cooking_range_cols, 'sum'),
        'pool_spa_pumps': (pool_spa_pumps_cols, 'sum'),
        'interior_lighting': (interior_lighting_cols, 'sum'),
        'exterior_lighting': (exterior_lighting_cols, 'sum'),
        'plug': (plug_cols, 'sum'),
        'pool_spa_heaters': (pool_spa_heaters_cols, 'sum')
    }
    
    # Initialize result dataframe
    result = grouped.sum()
    
    # Construct the new columns by summing the lists of columns
    for col_name, (src_cols, agg_func) in agg_dict.items():
        # Select only existing columns to avoid KeyError if some appliances are missing in some datasets
        existing_cols = [c for c in src_cols if c in df.columns]
        if existing_cols:
            result[col_name] = result[existing_cols].sum(axis=1)
        else:
            result[col_name] = 0.0
            
    # Calculate 'lighting' as sum of interior and exterior
    result['lighting'] = result['interior_lighting'] + result['exterior_lighting']
    
    # Reset index to make season and hour regular columns
    result = result.reset_index()
    
    # Select and order the target columns
    target_columns = [
        'season', 'hour', 'hvac', 'water_heating', 'refrigerator', 
        'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
        'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
        'lighting', 'plug', 'pool_spa_heaters'
    ]
    
    # Ensure all target columns exist
    for col in target_columns:
        if col not in result.columns:
            result[col] = 0.0
            
    return result[target_columns]