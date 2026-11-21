import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with 15-minute interval energy data
    into an hourly aggregated DataFrame grouped by month and hour.
    
    Categories:
    - hvac: Air conditioning, furnaces, heaters, house fans.
    - domestic_water_heating: Water heaters, circulation pumps.
    - major_appliances: Washers, dryers, dishwashers, ovens, ranges, fridges, microwaves, freezers.
    - lighting: Dedicated light circuits and outdoor/pool lights.
    - miscellaneous_plug_loads: Other room-specific loads, EVs, pools (non-light), security, etc.
    - total: Sum of all above categories.
    """
    
    # 1. Parse the timestamp
    df = source.copy()
    df['local_15min'] = pd.to_datetime(df['local_15min'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract grouping keys
    df['month'] = df['local_15min'].dt.month
    df['hour'] = df['local_15min'].dt.hour
    
    # 3. Define column mappings for each target category
    # Note: We only sum the '_sum' columns.
    
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum'
    ]
    
    dwh_cols = [
        'waterheater1_sum', 'waterheater2_sum',
        'circpump1_sum'
    ]
    
    major_appliances_cols = [
        'clotheswasher1_sum', 'clotheswasher_dryg1_sum',
        'dishwasher1_sum',
        'drye1_sum', 'dryg1_sum',
        'oven1_sum', 'oven2_sum',
        'range1_sum',
        'refrigerator1_sum', 'refrigerator2_sum',
        'microwave1_sum',
        'freezer1_sum'
    ]
    
    lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum',
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
        'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum',
        'poollight1_sum'
    ]
    
    misc_cols = [
        'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
        'bathroom1_sum', 'bathroom2_sum',
        'livingroom1_sum', 'livingroom2_sum',
        'kitchen1_sum', 'kitchen2_sum',
        'kitchenapp1_sum', 'kitchenapp2_sum',
        'diningroom1_sum', 'diningroom2_sum',
        'office1_sum',
        'garage1_sum', 'garage2_sum',
        'utilityroom1_sum', 'shed1_sum',
        'aquarium1_sum',
        'battery1_sum',
        'car1_sum', 'car2_sum',
        'disposal1_sum',
        'icemaker1_sum',
        'jacuzzi1_sum',
        'pool1_sum', 'pool2_sum',
        'poolpump1_sum',
        'pump1_sum',
        'sewerpump1_sum',
        'sumppump1_sum',
        'wellpump1_sum',
        'winecooler1_sum',
        'venthood1_sum',
        'security1_sum',
        'sprinkler1_sum'
    ]
    
    # 4. Aggregate by month and hour
    # We create a temporary dataframe for aggregation to avoid modifying the original index structure incorrectly
    agg_df = df.groupby(['month', 'hour']).agg({
        col: 'sum' for col in hvac_cols + dwh_cols + major_appliances_cols + lighting_cols + misc_cols
    }).reset_index()
    
    # 5. Calculate target columns
    agg_df['hvac'] = agg_df[hvac_cols].sum(axis=1)
    agg_df['domestic_water_heating'] = agg_df[dwh_cols].sum(axis=1)
    agg_df['major_appliances'] = agg_df[major_appliances_cols].sum(axis=1)
    agg_df['lighting'] = agg_df[lighting_cols].sum(axis=1)
    agg_df['miscellaneous_plug_loads'] = agg_df[misc_cols].sum(axis=1)
    
    # Total is the sum of all end-use categories
    agg_df['total'] = (
        agg_df['hvac'] + 
        agg_df['domestic_water_heating'] + 
        agg_df['major_appliances'] + 
        agg_df['lighting'] + 
        agg_df['miscellaneous_plug_loads']
    )
    
    # 6. Select and return the final columns
    target_columns = ['month', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    
    return agg_df[target_columns]