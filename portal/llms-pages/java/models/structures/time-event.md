# Time Event

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlRpbWVFdmVudA

TimeEvent.


# Class Name

`TimeEvent`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `At` | `String` | Required | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` | String getAt() | setAt(String at) |
| `Kind` | [`KindEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/kind.md) | Required | Kind. | KindEnum getKind() | setKind(KindEnum kind) |
| `Source` | [`Source5Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/source-5.md) | Required | Source. | Source5Enum getSource() | setSource(Source5Enum source) |


# Example

```java
import m18000.m0.m0.m127.models.KindEnum;
import m18000.m0.m0.m127.models.Source5Enum;
import m18000.m0.m0.m127.models.TimeEvent;

TimeEvent timeEvent = new TimeEvent.Builder(
    "at6",
    KindEnum.DELIVERY,
    Source5Enum.PROVIDER
)
.build();
```



