
-- This test ensures no messages have a post_date in the future
select *
from {{ ref('stg_telegram_messages') }}
where post_date > current_date
