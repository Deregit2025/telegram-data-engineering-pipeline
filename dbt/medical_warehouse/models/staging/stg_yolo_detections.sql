-- dbt/medical_warehouse/models/staging/stg_yolo_detections.sql

with base as (

    select
        message_id,
        channel_name,
        image_path,
        detected_class,
        confidence_score,
        -- replace empty or NULL values with 'other'
        case
            when image_category is null or image_category = '' then 'other'
            else image_category
        end as image_category
    from raw_yolo_detections

)

select *
from base
