# Policy Theme Counts

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlBvbGljeVRoZW1lQ291bnRz

PolicyThemeCounts.


# Class Name

`PolicyThemeCounts`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `disputeMediation` | `int` | Required | Dispute mediation.<br><br>**Constraints**: `>= 0`, `<= 29` | getDisputeMediation(): int | setDisputeMediation(int disputeMediation): void |
| `sourceCompliance` | `int` | Required | Source compliance.<br><br>**Constraints**: `>= 0`, `<= 29` | getSourceCompliance(): int | setSourceCompliance(int sourceCompliance): void |
| `velocityGuard` | `int` | Required | Velocity guard.<br><br>**Constraints**: `>= 0`, `<= 29` | getVelocityGuard(): int | setVelocityGuard(int velocityGuard): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\PolicyThemeCountsBuilder;

$policyThemeCounts = PolicyThemeCountsBuilder::init(
    29,
    29,
    29
)->build();
```



