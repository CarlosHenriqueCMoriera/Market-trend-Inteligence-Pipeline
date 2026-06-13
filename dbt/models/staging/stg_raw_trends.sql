{{
  config(
    materialized = "view",
    schema = "staging"
  )
}}

select
  id,
  keyword,
  value,
  date,
  region,
  collected_at
from {{ source("raw", "raw_trends") }}
where keyword is not null
