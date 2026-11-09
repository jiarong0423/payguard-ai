# Ai Brief Http Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkFpQnJpZWZIdHRwUmVxdWVzdA

What the console may send: the stage and, for disputes, which case. Session facts are never caller input.


# Class Name

`AiBriefHttpRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CaseRef` | [`AiBriefHttpRequestCaseRef`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/ai-brief-http-request-case-ref.md) | Optional | This is a container for any-of cases. | AiBriefHttpRequestCaseRef getCaseRef() | setCaseRef(AiBriefHttpRequestCaseRef caseRef) |
| `Stage` | [`StageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/stage.md) | Required | Stage. | StageEnum getStage() | setStage(StageEnum stage) |


# Example

```java
import m18000.m0.m0.m127.models.AiBriefHttpRequest;
import m18000.m0.m0.m127.models.StageEnum;
import m18000.m0.m0.m127.models.containers.AiBriefHttpRequestCaseRef;

AiBriefHttpRequest aiBriefHttpRequest = new AiBriefHttpRequest.Builder(
    StageEnum.VELOCITY_GUARD
)
.caseRef(AiBriefHttpRequestCaseRef.fromString(
        "String9"
    ))
.build();
```



