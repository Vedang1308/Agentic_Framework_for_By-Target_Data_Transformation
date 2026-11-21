import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by aggregating
    hourly electricity usage by season.
    """
    # 1. Parse time and create grouping keys
    df = source.copy()
    df['time_dt'] = pd.to_datetime(df['time'])
    df['hour'] = df['time_dt'].dt.hour
    
    # Define season based on month
    # Winter: Dec (12), Jan (1), Feb (2)
    # Spring: Mar (3), Apr (4), May (5)
    # Summer: Jun (6), Jul (7), Aug (8)
    # Autumn: Sep (9), Oct (10), Nov (11)
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

    # 2. Define column mappings and aggregations
    # We will sum the relevant columns. 
    # Note: We assume the base columns (e.g., electricity_cooling_kwh) are totals 
    # and do not add the 'central_system' subsets to avoid double counting.
    
    # Create intermediate columns for clarity and aggregation
    # HVAC: Sum of heating, cooling, and associated fans/pumps
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh'
    ]
    df['hvac'] = df[hvac_cols].sum(axis=1)
    
    # Water Heating
    df['water_heating'] = df['electricity_water_systems_kwh']
    
    # Refrigerator
    df['refrigerator'] = df['electricity_refrigerator_kwh']
    
    # Clothes Washer
    df['clothes_washer'] = df['electricity_clothes_washer_kwh']
    
    # Clothes Dryer
    df['clothes_dryer'] = df['electricity_clothes_dryer_kwh']
    
    # Dishwasher
    df['dishwasher'] = df['electricity_dishwasher_kwh']
    
    # Cooking Range
    df['cooking_range'] = df['electricity_cooking_range_kwh']
    
    # Pool/Spa Pumps: Sum of pool pump and hot tub pump
    df['pool_spa_pumps'] = df['electricity_pool_pump_kwh'] + df['electricity_hot_tub_pump_kwh']
    
    # Interior Lighting
    df['interior_lighting'] = df['electricity_interior_lighting_kwh']
    
    # Exterior Lighting
    df['exterior_lighting'] = df['electricity_exterior_lighting_kwh']
    
    # Total Lighting
    df['lighting'] = df['interior_lighting'] + df['exterior_lighting']
    
    # Plug Loads
    df['plug'] = df['electricity_plug_loads_kwh']
    
    # Pool/Spa Heaters: Sum of pool heater and hot tub heater
    df['pool_spa_heaters'] = df['electricity_pool_heater_kwh'] + df['electricity_hot_tub_heater_kwh']

    # 3. Group by season and hour, and sum the values
    target_columns = [
        'season', 'hour', 'hvac', 'water_heating', 'refrigerator', 
        'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
        'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
        'lighting', 'plug', 'pool_spa_heaters'
    ]
    
    # Select only the columns we need for aggregation
    agg_cols = [c for c in target_columns if c not in ['season', 'hour']]
    
    # Group and sum
    df_agg = df.groupby(['season', 'hour'])[agg_cols].sum().reset_index()

    # 4. Ensure column order matches target
    # Sort by season (optional but good for consistency) and hour
    # Define season order for sorting
    season_order = ['Winter', 'Spring', 'Summer', 'Autumn']
    df_agg['season_order'] = df_agg['season'].map({s: i for i, s in enumerate(season_order)})
    df_agg = df_agg.sort_values(['season_order', 'hour']).drop(columns=['season_order'])

    return df_agg[target_columns]