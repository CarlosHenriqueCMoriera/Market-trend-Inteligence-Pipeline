{{
  config(
    materialized = "table",
    schema = "marts"
  )
}}

with stats as (
  select
    keyword,
    region,
    min(value) as min_value,
    max(value) as max_value,
    avg(value) as avg_value,
    count(*) as total_records,
    min(date) as first_date,
    max(date) as last_date
  from {{ ref("stg_raw_trends") }}
  group by keyword, region
)

select
  *,
  max_value - min_value as value_range
from stats
order by avg_value desc
