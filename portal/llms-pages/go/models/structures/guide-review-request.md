# Guide Review Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3UmVxdWVzdA

GuideReviewRequest.


# Class Name

`GuideReviewRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Change` | `[]string` | Optional | Change.<br><br>**Constraints**: *Maximum Items*: `9`, *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z_]+$` |
| `Confirm` | `*bool` | Optional | Confirm.<br><br>**Default**: `false` |
| `Scenario` | [`*models.GuideReviewRequestScenario`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/guide-review-request-scenario.md) | Optional | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideReviewRequest := models.GuideReviewRequest{
        Change:   []string{
            "change9",
            "change0",
            "change1",
        },
        Confirm:  models.ToPointer(false),
        Scenario: models.ToPointer(models.GuideReviewRequestScenarioContainer.FromScenario1(models.Scenario1Enum_DISPUTE)),
    }

}
```



