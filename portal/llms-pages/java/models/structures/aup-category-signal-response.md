# Aup Category Signal Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVzcG9uc2U

Optional Channel3 signal shown next to the AUP result; it never changes the rule decision.


# Class Name

`AupCategorySignalResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AffectsDecision` | `String` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` | String getAffectsDecision() | setAffectsDecision(String affectsDecision) |
| `Reason` | [`AupCategorySignalResponseReason`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/aup-category-signal-response-reason.md) | Required | This is a container for any-of cases. | AupCategorySignalResponseReason getReason() | setReason(AupCategorySignalResponseReason reason) |
| `Signal` | [`AupCategorySignalResponseSignal`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/aup-category-signal-response-signal.md) | Required | This is a container for any-of cases. | AupCategorySignalResponseSignal getSignal() | setSignal(AupCategorySignalResponseSignal signal) |
| `Status` | [`Status2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/status-2.md) | Required | Status. | Status2Enum getStatus() | setStatus(Status2Enum status) |


# Example

```java
import m18000.m0.m0.m127.models.AupCategorySignalResponse;
import m18000.m0.m0.m127.models.CategorySignal;
import m18000.m0.m0.m127.models.ConfidenceEnum;
import m18000.m0.m0.m127.models.ReasonEnum;
import m18000.m0.m0.m127.models.Status2Enum;
import m18000.m0.m0.m127.models.containers.AupCategorySignalResponseReason;
import m18000.m0.m0.m127.models.containers.AupCategorySignalResponseSignal;
import m18000.m0.m0.m127.models.containers.CategorySignalCategory;
import m18000.m0.m0.m127.models.containers.CategorySignalConfidence;

AupCategorySignalResponse aupCategorySignalResponse = new AupCategorySignalResponse.Builder(
    "False",
    AupCategorySignalResponseReason.fromReason(
        ReasonEnum.BUDGET_EXHAUSTED
    ),
    AupCategorySignalResponseSignal.fromCategorySignal(
        new CategorySignal.Builder(
            CategorySignalCategory.fromString(
                "String9"
            ),
            CategorySignalConfidence.fromConfidence(
                ConfidenceEnum.HIGH
            ),
            "channel3"
        )
        .build()
    ),
    Status2Enum.NOT_SENT
)
.build();
```



