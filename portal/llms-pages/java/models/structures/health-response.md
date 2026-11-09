# Health Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkhlYWx0aFJlc3BvbnNl

HealthResponse.


# Class Name

`HealthResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Mode` | `String` | Required, Constant | Mode.<br><br>**Value**: `"demo"` | String getMode() | setMode(String mode) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` | String getSource() | setSource(String source) |
| `Status` | `String` | Required, Constant | Status.<br><br>**Value**: `"ok"` | String getStatus() | setStatus(String status) |
| `Version` | `String` | Required | Version. | String getVersion() | setVersion(String version) |


# Example

```java
import m18000.m0.m0.m127.models.HealthResponse;

HealthResponse healthResponse = new HealthResponse.Builder(
    "demo",
    "synthetic",
    "ok",
    "version0"
)
.build();
```



