import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse datetime
    df['dt'] = pd.to_datetime(df['local_15min'], format='%m/%d/%Y %H:%M')
    df['hour'] = df['dt'].dt.hour
    df['month'] = df['dt'].dt.month
    
    # 2. Determine Season
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    df['season'] = df['month'].apply(get_season)
    
    # 3. Define Column Mappings for Aggregation
    # HVAC
    hvac_cols = ['air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum', 
                 'furnace1_sum', 'furnace2_sum', 'heater1_sum', 'heater2_sum', 
                 'heater3_sum', 'housefan1_sum']
    
    # Water Heating
    water_heating_cols = ['waterheater1_sum', 'waterheater2_sum']
    
    # Refrigerator
    refrigerator_cols = ['refrigerator1_sum', 'refrigerator2_sum', 'freezer1_sum', 
                         'icemaker1_sum', 'winecooler1_sum']
    
    # Clothes Washer
    clothes_washer_cols = ['clotheswasher1_sum', 'clotheswasher_dryg1_sum']
    
    # Clothes Dryer
    clothes_dryer_cols = ['drye1_sum', 'dryg1_sum']
    
    # Dishwasher
    dishwasher_cols = ['dishwasher1_sum', 'disposal1_sum']
    
    # Cooking Range
    cooking_range_cols = ['oven1_sum', 'oven2_sum', 'range1_sum', 'microwave1_sum', 'venthood1_sum']
    
    # Pool/Spa Pumps
    pool_spa_pumps_cols = ['poolpump1_sum', 'pool1_sum', 'pool2_sum', 'circpump1_sum', 
                           'pump1_sum', 'sewerpump1_sum', 'sumppump1_sum', 'wellpump1_sum', 'sprinkler1_sum']
    
    # Pool/Spa Heaters
    pool_spa_heaters_cols = ['jacuzzi1_sum']
    
    # Interior Lighting
    interior_lighting_cols = ['bathroom1_sum', 'bathroom2_sum', 'bedroom1_sum', 'bedroom2_sum', 
                              'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum', 'diningroom1_sum', 
                              'diningroom2_sum', 'kitchen1_sum', 'kitchen2_sum', 'livingroom1_sum', 
                              'livingroom2_sum', 'office1_sum', 'utilityroom1_sum', 'garage1_sum', 
                              'garage2_sum', 'shed1_sum']
    
    # Exterior Lighting
    exterior_lighting_cols = ['poollight1_sum']
    
    # Plug Loads
    plug_cols = ['lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 'lights_plugs4_sum',
                 'lights_plugs5_sum', 'lights_plugs6_sum', 'kitchenapp1_sum', 'kitchenapp2_sum',
                 'car1_sum', 'car2_sum', 'battery1_sum', 'aquarium1_sum', 'security1_sum',
                 'solar_sum', 'solar2_sum']

    # 4. Calculate Aggregated Columns
    df['hvac'] = df[hvac_cols].sum(axis=1)
    df['water_heating'] = df[water_heating_cols].sum(axis=1)
    df['refrigerator'] = df[refrigerator_cols].sum(axis=1)
    df['clothes_washer'] = df[clothes_washer_cols].sum(axis=1)
    df['clothes_dryer'] = df[clothes_dryer_cols].sum(axis=1)
    df['dishwasher'] = df[dishwasher_cols].sum(axis=1)
    df['cooking_range'] = df[cooking_range_cols].sum(axis=1)
    df['pool_spa_pumps'] = df[pool_spa_pumps_cols].sum(axis=1)
    df['pool_spa_heaters'] = df[pool_spa_heaters_cols].sum(axis=1)
    df['interior_lighting'] = df[interior_lighting_cols].sum(axis=1)
    df['exterior_lighting'] = df[exterior_lighting_cols].sum(axis=1)
    df['plug'] = df[plug_cols].sum(axis=1)
    
    # Lighting is sum of interior and exterior based on target sample equality
    df['lighting'] = df['interior_lighting'] + df['exterior_lighting']
    
    # 5. Group and Aggregate
    # The target has one row per Season/Hour combination.
    agg_dict = {
        'hvac': 'sum',
        'water_heating': 'sum',
        'refrigerator': 'sum',
        'clothes_washer': 'sum',
        'clothes_dryer': 'sum',
        'dishwasher': 'sum',
        'cooking_range': 'sum',
        'pool_spa_pumps': 'sum',
        'pool_spa_heaters': 'sum',
        'interior_lighting': 'sum',
        'exterior_lighting': 'sum',
        'lighting': 'sum',
        'plug': 'sum'
    }
    
    result = df.groupby(['season', 'hour']).agg(agg_dict).reset_index()
    
    # 6. Select and Order Columns
    target_columns = ['season', 'hour', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 
                      'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 
                      'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heaters']
    
    return result[target_columns]