# Policy Theme Counts

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlBvbGljeVRoZW1lQ291bnRz

PolicyThemeCounts.


# Class Name

`PolicyThemeCounts`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `DisputeMediation` | `int` | Required | Dispute mediation.<br><br>**Constraints**: `>= 0`, `<= 29` | int getDisputeMediation() | setDisputeMediation(int disputeMediation) |
| `SourceCompliance` | `int` | Required | Source compliance.<br><br>**Constraints**: `>= 0`, `<= 29` | int getSourceCompliance() | setSourceCompliance(int sourceCompliance) |
| `VelocityGuard` | `int` | Required | Velocity guard.<br><br>**Constraints**: `>= 0`, `<= 29` | int getVelocityGuard() | setVelocityGuard(int velocityGuard) |


# Example

```java
import m18000.m0.m0.m127.models.PolicyThemeCounts;

PolicyThemeCounts policyThemeCounts = new PolicyThemeCounts.Builder(
    29,
    29,
    29
)
.build();
```



