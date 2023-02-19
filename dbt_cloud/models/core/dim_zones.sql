{{ config(materialized='table') }}

select
    LocationID,
    Borough,
    Zone,
    replace(service_zone, 'Boro', 'Green') as service_zone                -- change the "Boro" value in this column
from {{ ref('taxi_zone_lookup') }}
