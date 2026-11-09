# Ai Brief Http Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkFpQnJpZWZIdHRwUmVxdWVzdA

What the console may send: the stage and, for disputes, which case. Session facts are never caller input.


# Class Name

`AiBriefHttpRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CaseRef` | [`*models.AiBriefHttpRequestCaseRef`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/ai-brief-http-request-case-ref.md) | Optional | This is a container for any-of cases. |
| `Stage` | [`models.StageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/stage.md) | Required | Stage. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    aiBriefHttpRequest := models.AiBriefHttpRequest{
        CaseRef: models.ToPointer(models.AiBriefHttpRequestCaseRefContainer.FromString("String9")),
        Stage:   models.StageEnum_VELOCITYGUARD,
    }

}
```



