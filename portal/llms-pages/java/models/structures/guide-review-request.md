# Guide Review Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3UmVxdWVzdA

GuideReviewRequest.


# Class Name

`GuideReviewRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Change` | `List<String>` | Optional | Change.<br><br>**Constraints**: *Maximum Items*: `9`, *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z_]+$` | List<String> getChange() | setChange(List<String> change) |
| `Confirm` | `Boolean` | Optional | Confirm.<br><br>**Default**: `false` | Boolean getConfirm() | setConfirm(Boolean confirm) |
| `Scenario` | [`GuideReviewRequestScenario`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/guide-review-request-scenario.md) | Optional | This is a container for any-of cases. | GuideReviewRequestScenario getScenario() | setScenario(GuideReviewRequestScenario scenario) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.GuideReviewRequest;
import m18000.m0.m0.m127.models.Scenario1Enum;
import m18000.m0.m0.m127.models.containers.GuideReviewRequestScenario;

GuideReviewRequest guideReviewRequest = new GuideReviewRequest.Builder()
    .change(Arrays.asList(
        "change9",
        "change0",
        "change1"
    ))
    .confirm(false)
    .scenario(GuideReviewRequestScenario.fromScenario1(
        Scenario1Enum.DISPUTE
    ))
    .build();
```



