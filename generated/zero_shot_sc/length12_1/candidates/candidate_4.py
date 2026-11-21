import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse time and extract features
    df = source.copy()
    df['time_dt'] = pd.to_datetime(df['time'])
    df['hour'] = df['time_dt'].dt.hour
    df['month'] = df['time_dt'].dt.month
    
    # 2. Map month to season
    # Winter: 12, 1, 2
    # Spring: 3, 4, 5
    # Summer: 6, 7, 8
    # Fall: 9, 10, 11
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
    
    # 3. Construct target columns from source columns
    # HVAC: Sum of heating, cooling, and their associated fans/pumps
    # Note: Using the top-level heating/cooling columns which likely include central systems
    df['hvac'] = (
        df['electricity_heating_kwh'] +
        df['electricity_cooling_kwh'] +
        df['electricity_fans_heating_kwh'] +
        df['electricity_fans_cooling_kwh'] +
        df['electricity_pumps_heating_kwh'] +
        df['electricity_pumps_cooling_kwh']
    )
    
    # Water Heating
    df['water_heating'] = df['electricity_water_systems_kwh']
    
    # Appliances (Direct mapping)
    df['refrigerator'] = df['electricity_refrigerator_kwh']
    df['clothes_washer'] = df['electricity_clothes_washer_kwh']
    df['clothes_dryer'] = df['electricity_clothes_dryer_kwh']
    df['dishwasher'] = df['electricity_dishwasher_kwh']
    df['cooking_range'] = df['electricity_cooking_range_kwh']
    df['plug'] = df['electricity_plug_loads_kwh']
    
    # Pool/Spa Pumps
    df['pool_spa_pumps'] = (
        df['electricity_pool_pump_kwh'] +
        df['electricity_hot_tub_pump_kwh']
    )
    
    # Lighting
    df['interior_lighting'] = df['electricity_interior_lighting_kwh']
    df['exterior_lighting'] = df['electricity_exterior_lighting_kwh']
    df['lighting'] = df['interior_lighting'] + df['exterior_lighting']
    
    # Pool/Spa Heaters
    df['pool_spa_heaters'] = (
        df['electricity_pool_heater_kwh'] +
        df['electricity_hot_tub_heater_kwh']
    )
    
    # 4. Aggregate by season and hour
    target_columns = [
        'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 
        'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 
        'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 
        'pool_spa_heaters'
    ]
    
    grouped = df.groupby(['season', 'hour'])[target_columns].sum()
    
    # 5. Format the result
    result = grouped.reset_index()
    
    # Ensure column order matches target
    final_columns = [
        'season', 'hour', 'hvac', 'water_heating', 'refrigerator', 
        'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
        'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
        'lighting', 'plug', 'pool_spa_heaters'
    ]
    
    return result[final_columns]