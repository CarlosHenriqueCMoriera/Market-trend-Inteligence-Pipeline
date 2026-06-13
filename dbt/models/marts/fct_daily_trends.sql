{{
  config(
    materialized = "table",
    schema = "marts"
  )
}}

with trends as (
  select
    keyword,
    date,
    value,
    region
  from {{ ref("stg_raw_trends") }}
)

select
  keyword,
  date,
  value,
  region,
  avg(value) over (partition by keyword order by date rows between 6 preceding and current row) as moving_avg_7d
from trends
