# Guide Gap

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkd1aWRlR2Fw

GuideGap.


# Class Name

`GuideGap`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Conflicting` | `List<String>` | Required | Conflicting. | List<String> getConflicting() | setConflicting(List<String> conflicting) |
| `Missing` | `List<String>` | Required | Missing. | List<String> getMissing() | setMissing(List<String> missing) |
| `Partial` | `List<String>` | Required | Partial. | List<String> getPartial() | setPartial(List<String> partial) |
| `Present` | `List<String>` | Required | Present. | List<String> getPresent() | setPresent(List<String> present) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.GuideGap;

GuideGap guideGap = new GuideGap.Builder(
    Arrays.asList(
        "conflicting9"
    ),
    Arrays.asList(
        "missing4"
    ),
    Arrays.asList(
        "partial4",
        "partial5"
    ),
    Arrays.asList(
        "present9",
        "present0",
        "present1"
    )
)
.build();
```



