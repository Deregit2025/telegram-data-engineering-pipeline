-- models/staging/stg_telegram_messages.sql

{{ config(
    materialized='view'
) }}

with raw as (

    select *
    from {{ source('raw', 'telegram_messages') }}

),

cleaned as (

    select
        message_id,
        channel_name,
        post_date::timestamp as post_date,
        message_text,
        coalesce(view_count, 0)::int as view_count,
        coalesce(forward_count, 0)::int as forward_count,
        case 
            when has_image is null then false
            else has_image
        end as has_image,
        length(message_text) as message_length,
        raw_json
    from raw
    where message_id is not null
      and post_date is not null
      and message_text is not null

)

select * from cleaned
