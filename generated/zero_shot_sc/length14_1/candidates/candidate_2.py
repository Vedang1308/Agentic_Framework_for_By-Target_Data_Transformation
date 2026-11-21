import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source electricity usage DataFrame into a monthly/hourly aggregated summary.
    """
    # 1. Parse the time column
    df = source.copy()
    df['time'] = pd.to_datetime(df['time'])
    
    # 2. Extract month and hour for grouping
    df['month'] = df['time'].dt.month
    df['hour'] = df['time'].dt.hour
    
    # 3. Define source columns for each target category
    
    # HVAC: Heating, Cooling, Fans, Pumps related to HVAC systems
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
    dwh_cols = [
        'electricity_water_systems_kwh'
    ]
    
    # Major Appliances: Kitchen and Laundry
    major_appl_cols = [
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
    
    # Miscellaneous Plug Loads: Remaining loads (general plugs, other fans, pool/hot tub)
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
    
    # Total
    total_cols = [
        'net_site_electricity_kwh'
    ]
    
    # 4. Create aggregated columns by summing the respective source columns
    # We sum across the columns for each row first, then we will aggregate by time.
    # Actually, it's more efficient to group first then sum, or sum then group. 
    # Given the structure, let's create the category columns first.
    
    df['hvac'] = df[hvac_cols].sum(axis=1)
    df['domestic_water_heating'] = df[dwh_cols].sum(axis=1)
    df['major_appliances'] = df[major_appl_cols].sum(axis=1)
    df['lighting'] = df[lighting_cols].sum(axis=1)
    df['miscellaneous_plug_loads'] = df[misc_cols].sum(axis=1)
    df['total'] = df[total_cols].sum(axis=1)
    
    # 5. Group by month and hour and sum the values
    # The target requires aggregation of all 15-min intervals into month/hour buckets.
    agg_df = df.groupby(['month', 'hour'], as_index=False).agg({
        'hvac': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum',
        'total': 'sum'
    })
    
    # 6. Define target columns in the exact order required
    target_columns = [
        'month', 
        'hour', 
        'hvac', 
        'domestic_water_heating', 
        'major_appliances', 
        'lighting', 
        'miscellaneous_plug_loads', 
        'total'
    ]
    
    # 7. Return the DataFrame with the correct schema
    return agg_df[target_columns]