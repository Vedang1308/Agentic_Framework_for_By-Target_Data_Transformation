import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source electricity usage DataFrame into a summarized 
    DataFrame grouped by season and hour.
    """
    # 1. Parse the time column
    df = source.copy()
    df['time'] = pd.to_datetime(df['time'])
    
    # 2. Extract hour and month
    df['hour'] = df['time'].dt.hour
    df['month'] = df['time'].dt.month
    
    # 3. Determine Season
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
            
    df['season'] = df['month'].apply(get_season)
    
    # 4. Define Category Sums
    # HVAC: Heating, Cooling, and their associated fans/pumps
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_central_system_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_central_system_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_central_system_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_pumps_cooling_kwh'
    ]
    df['hvac'] = df[hvac_cols].sum(axis=1)
    
    # Domestic Water Heating
    # Typically just the water systems column in this dataset structure
    df['domestic_water_heating'] = df['electricity_water_systems_kwh']
    
    # Major Appliances
    major_appliance_cols = [
        'electricity_refrigerator_kwh',
        'electricity_clothes_washer_kwh',
        'electricity_clothes_dryer_kwh',
        'electricity_cooking_range_kwh',
        'electricity_dishwasher_kwh'
    ]
    df['major_appliances'] = df[major_appliance_cols].sum(axis=1)
    
    # Lighting
    lighting_cols = [
        'electricity_interior_lighting_kwh',
        'electricity_exterior_lighting_kwh'
    ]
    df['lighting'] = df[lighting_cols].sum(axis=1)
    
    # Miscellaneous Plug Loads
    # Includes general plug loads, various fans, and pool/hot tub equipment
    misc_cols = [
        'electricity_plug_loads_kwh',
        'electricity_house_fan_kwh',
        'electricity_range_fan_kwh',
        'electricity_bath_fan_kwh',
        'electricity_ceiling_fan_kwh',
        'electricity_pool_heater_kwh',
        'electricity_pool_pump_kwh',
        'electricity_hot_tub_heater_kwh',
        'electricity_hot_tub_pump_kwh'
    ]
    df['miscellaneous_plug_loads'] = df[misc_cols].sum(axis=1)
    
    # Total
    df['total'] = df['net_site_electricity_kwh']
    
    # 5. Group by Season and Hour, then Sum
    target_columns = ['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    
    # Select only the necessary columns for grouping to avoid confusion
    agg_df = df.groupby(['season', 'hour'], as_index=False)[
        ['hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    ].sum()
    
    # 6. Ensure column order matches target
    return agg_df[target_columns]