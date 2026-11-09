# Document Redaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkRvY3VtZW50UmVkYWN0aW9u

DocumentRedaction.


# Class Name

`DocumentRedaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Counts` | `map[string]int` | Required | Counts.<br><br>**Constraints**: `>= 1`, `<= 128` |
| `ExportProfile` | `string` | Required, Constant | Export profile.<br><br>**Value**: `"INTERNAL_REVIEW_ONLY_V1"` |
| `Limitations` | `[]string` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `8`, *Minimum Length*: `1`, *Maximum Length*: `1000` |
| `LimitedDetection` | `string` | Required, Constant | Limited detection.<br><br>**Value**: `"True"` |
| `ManualReviewRequired` | `string` | Required, Constant | Manual review required.<br><br>**Value**: `"True"` |
| `Method` | `string` | Required, Constant | Method.<br><br>**Value**: `"HMAC-SHA256 document pseudonymization v1"` |
| `RedactedText` | `string` | Required | Redacted text.<br><br>**Constraints**: *Maximum Length*: `32768` |
| `ReplacementCount` | `int` | Required | Replacement count.<br><br>**Constraints**: `>= 0`, `<= 128` |
| `Reversibility` | `string` | Required, Constant | Reversibility.<br><br>**Value**: `"False"` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `Types` | [`[]models.TypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/type.md) | Required | Types.<br><br>**Constraints**: *Maximum Items*: `7` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    documentRedaction := models.DocumentRedaction{
        Counts:               map[string]int{
            "key0": 128,
            "key1": 1,
            "key2": 1,
        },
        ExportProfile:        "INTERNAL_REVIEW_ONLY_V1",
        Limitations:          []string{
            "limitations3",
        },
        LimitedDetection:     "True",
        ManualReviewRequired: "True",
        Method:               "HMAC-SHA256 document pseudonymization v1",
        RedactedText:         "redacted_text2",
        ReplacementCount:     128,
        Reversibility:        "False",
        Source:               "synthetic",
        Types:                []models.TypeEnum{
            models.TypeEnum_IDLIKE,
            models.TypeEnum_NAME,
            models.TypeEnum_ADDRESS,
        },
    }

}
```



