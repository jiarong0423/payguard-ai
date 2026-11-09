# Observation Status

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRk9ic2VydmF0aW9uU3RhdHVz

Observation status.


# Enum Type Name

`ObservationStatusEnum`


# Fields

| Name |
|  --- |
| `FUTURE_OBSERVATION` |
| `STALE_OBSERVATION` |
| `WITHIN_OBSERVATION_BUDGET` |


# Example

```php
use TradeGlotLocalConsoleLib\Models\ObservationStatusEnum;

$observationStatus = ObservationStatusEnum::FUTURE_OBSERVATION;
```



