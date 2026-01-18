-- models/marts/dim_channels.sql
{{ config(materialized='table') }}

with channels as (
    select
        dense_rank() over (order by channel_name) as channel_key,  -- surrogate key
        channel_name,
        case
            when channel_name = 'chemed' then 'Medical'
            when channel_name = 'lobelia_cosmetics' then 'Cosmetics'
            when channel_name = 'tikvah_pharma' then 'Pharmaceutical'
            else 'Unknown'
        end as channel_type,
        min(post_date) as first_post_date,
        max(post_date) as last_post_date,
        count(*) as total_posts,
        avg(view_count) as avg_views
    from {{ ref('stg_telegram_messages') }}
    group by channel_name
)

select * from channels
