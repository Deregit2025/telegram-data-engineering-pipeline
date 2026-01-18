-- dbt/medical_warehouse/models/marts/fct_image_detections.sql

with yolo_clean as (
    select
        -- normalize message_id to match fct_messages
        regexp_replace(message_id, '^[^0-9]*', '')::int as message_id_clean,
        detected_class,
        confidence_score,
        case
            when image_category is null or image_category = '' then 'other'
            else image_category
        end as image_category
    from {{ ref('stg_yolo_detections') }}
),

yolo_agg as (
    select
        message_id_clean as message_id,
        string_agg(distinct detected_class, ', ') as detected_class,
        max(confidence_score) as confidence_score,
        -- classify images based on detected classes
        case
            when 'person' = any(array_agg(distinct detected_class)) 
                 and ('bottle' = any(array_agg(distinct detected_class))
                      or 'product' = any(array_agg(distinct detected_class))) then 'promotional'
            when 'person' = any(array_agg(distinct detected_class)) then 'lifestyle'
            when 'bottle' = any(array_agg(distinct detected_class))
                 or 'product' = any(array_agg(distinct detected_class)) then 'product_display'
            else 'other'
        end as image_category
    from yolo_clean
    group by message_id_clean
)

select
    y.message_id,
    m.channel_key,
    m.date_key,
    y.detected_class,
    y.confidence_score,
    y.image_category
from yolo_agg y
left join {{ ref('fct_messages') }} m
    on y.message_id::text = m.message_id
