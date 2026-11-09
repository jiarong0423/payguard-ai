# Inject Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkluamVjdFJlcXVlc3Q

InjectRequest.


# Class Name

`InjectRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Scenario` | [`Scenario5Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/scenario-5.md) | Required | Scenario. | Scenario5Enum getScenario() | setScenario(Scenario5Enum scenario) |


# Example

```java
import m18000.m0.m0.m127.models.InjectRequest;
import m18000.m0.m0.m127.models.Scenario5Enum;

InjectRequest injectRequest = new InjectRequest.Builder(
    Scenario5Enum.BURST
)
.build();
```



