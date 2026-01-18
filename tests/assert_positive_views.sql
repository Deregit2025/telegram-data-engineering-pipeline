-- tests/assert_positive_views.sql
-- Ensures all view counts are 0 or more
select *
from {{ ref('stg_telegram_messages') }}
where view_count < 0
