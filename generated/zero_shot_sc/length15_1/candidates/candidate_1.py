import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source electricity usage table into a summarized table
    aggregated by season and hour.
    """
    df = source.copy()
    
    # 1. Parse time and extract hour and season
    df['time'] = pd.to_datetime(df['time'])
    df['hour'] = df['time'].dt.hour
    
    # Define season based on month (Meteorological seasons)
    # Winter: Dec(12), Jan(1), Feb(2)
    # Spring: Mar(3), Apr(4), May(5)
    # Summer: Jun(6), Jul(7), Aug(8)
    # Fall: Sep(9), Oct(10), Nov(11)
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    df['season'] = df['time'].dt.month.apply(get_season)

    # 2. Define column groups for aggregation
    
    # HVAC Components
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
    
    # Domestic Water Heating
    # In this dataset, 'electricity_water_systems_kwh' is the standard column for water heating
    df['domestic_water_heating'] = df['electricity_water_systems_kwh']
    
    # Major Appliances
    major_appliances_cols = [
        'electricity_refrigerator_kwh',
        'electricity_clothes_washer_kwh',
        'electricity_clothes_dryer_kwh',
        'electricity_cooking_range_kwh',
        'electricity_dishwasher_kwh'
    ]
    
    # Lighting
    lighting_cols = [
        'electricity_interior_lighting_kwh',
        'electricity_exterior_lighting_kwh'
    ]
    
    # Miscellaneous Plug Loads
    misc_plug_cols = [
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
    
    # Total
    df['total'] = df['net_site_electricity_kwh']
    
    # 3. Sum the components for each category
    # Handle potential missing columns by checking existence, though schema implies they exist
    def safe_sum(cols):
        existing_cols = [c for c in cols if c in df.columns]
        if not existing_cols:
            return pd.Series(0, index=df.index)
        return df[existing_cols].sum(axis=1)

    df['hvac'] = safe_sum(hvac_cols)
    df['major_appliances'] = safe_sum(major_appliances_cols)
    df['lighting'] = safe_sum(lighting_cols)
    df['miscellaneous_plug_loads'] = safe_sum(misc_plug_cols)

    # 4. Group by season and hour, and sum the aggregated values
    target_columns = ['season', 'hour', 'hvac', 'domestic_water_heating', 
                      'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    
    # Ensure all aggregation columns are numeric
    agg_cols = ['hvac', 'domestic_water_heating', 'major_appliances', 
                'lighting', 'miscellaneous_plug_loads', 'total']
    
    for col in agg_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Group and aggregate
    result = df.groupby(['season', 'hour'], as_index=False)[agg_cols].sum()
    
    # 5. Return the result with exact column names
    return result[target_columns]