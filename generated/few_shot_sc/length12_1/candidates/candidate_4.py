import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse time and extract hour and season
    df['time_dt'] = pd.to_datetime(df['time'])
    df['hour'] = df['time_dt'].dt.hour
    
    # Determine season based on month
    # Winter: 12, 1, 2
    # Spring: 3, 4, 5
    # Summer: 6, 7, 8
    # Autumn: 9, 10, 11
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Autumn'
            
    df['season'] = df['time_dt'].dt.month.apply(get_season)
    
    # 2. Calculate intermediate aggregated columns
    # hvac: Sum of heating, cooling, fans, and pumps
    df['hvac_raw'] = (df['electricity_heating_kwh'] + 
                      df['electricity_cooling_kwh'] + 
                      df['electricity_fans_heating_kwh'] + 
                      df['electricity_fans_cooling_kwh'] + 
                      df['electricity_pumps_heating_kwh'] + 
                      df['electricity_pumps_cooling_kwh'])
    
    # water_heating
    df['water_heating_raw'] = df['electricity_water_systems_kwh']
    
    # refrigerator
    df['refrigerator_raw'] = df['electricity_refrigerator_kwh']
    
    # clothes_washer
    df['clothes_washer_raw'] = df['electricity_clothes_washer_kwh']
    
    # clothes_dryer
    df['clothes_dryer_raw'] = df['electricity_clothes_dryer_kwh']
    
    # dishwasher
    df['dishwasher_raw'] = df['electricity_dishwasher_kwh']
    
    # cooking_range
    df['cooking_range_raw'] = df['electricity_cooking_range_kwh']
    
    # pool_spa_pumps: pool pump + hot tub pump
    df['pool_spa_pumps_raw'] = df['electricity_pool_pump_kwh'] + df['electricity_hot_tub_pump_kwh']
    
    # interior_lighting
    df['interior_lighting_raw'] = df['electricity_interior_lighting_kwh']
    
    # exterior_lighting
    df['exterior_lighting_raw'] = df['electricity_exterior_lighting_kwh']
    
    # lighting: sum of interior and exterior
    df['lighting_raw'] = df['interior_lighting_raw'] + df['exterior_lighting_raw']
    
    # plug
    df['plug_raw'] = df['electricity_plug_loads_kwh']
    
    # pool_spa_heaters: pool heater + hot tub heater
    df['pool_spa_heaters_raw'] = df['electricity_pool_heater_kwh'] + df['electricity_hot_tub_heater_kwh']
    
    # 3. Aggregate by season and hour
    agg_cols = {
        'hvac_raw': 'hvac',
        'water_heating_raw': 'water_heating',
        'refrigerator_raw': 'refrigerator',
        'clothes_washer_raw': 'clothes_washer',
        'clothes_dryer_raw': 'clothes_dryer',
        'dishwasher_raw': 'dishwasher',
        'cooking_range_raw': 'cooking_range',
        'pool_spa_pumps_raw': 'pool_spa_pumps',
        'interior_lighting_raw': 'interior_lighting',
        'exterior_lighting_raw': 'exterior_lighting',
        'lighting_raw': 'lighting',
        'plug_raw': 'plug',
        'pool_spa_heaters_raw': 'pool_spa_heaters'
    }
    
    # Group by season and hour, sum the raw columns
    grouped = df.groupby(['season', 'hour'], as_index=False).agg(agg_cols)
    
    # 4. Sort and format
    # Sort by season (alphabetical) and hour to ensure deterministic output
    # Note: The target sample order is not strictly alphabetical, but standard practice is sorted.
    # If the target implies a specific order, we might need to adjust. 
    # Given the randomness in the sample snippet, sorted is the safest generalization.
    grouped = grouped.sort_values(['season', 'hour']).reset_index(drop=True)
    
    # Ensure column order matches target
    target_columns = ['season', 'hour', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heaters']
    
    return grouped[target_columns]