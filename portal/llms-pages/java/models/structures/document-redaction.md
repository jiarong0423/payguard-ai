# Document Redaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkRvY3VtZW50UmVkYWN0aW9u

DocumentRedaction.


# Class Name

`DocumentRedaction`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Counts` | `Map<String, Integer>` | Required | Counts.<br><br>**Constraints**: `>= 1`, `<= 128` | Map<String, Integer> getCounts() | setCounts(Map<String, Integer> counts) |
| `ExportProfile` | `String` | Required, Constant | Export profile.<br><br>**Value**: `"INTERNAL_REVIEW_ONLY_V1"` | String getExportProfile() | setExportProfile(String exportProfile) |
| `Limitations` | `List<String>` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `8`, *Minimum Length*: `1`, *Maximum Length*: `1000` | List<String> getLimitations() | setLimitations(List<String> limitations) |
| `LimitedDetection` | `String` | Required, Constant | Limited detection.<br><br>**Value**: `"True"` | String getLimitedDetection() | setLimitedDetection(String limitedDetection) |
| `ManualReviewRequired` | `String` | Required, Constant | Manual review required.<br><br>**Value**: `"True"` | String getManualReviewRequired() | setManualReviewRequired(String manualReviewRequired) |
| `Method` | `String` | Required, Constant | Method.<br><br>**Value**: `"HMAC-SHA256 document pseudonymization v1"` | String getMethod() | setMethod(String method) |
| `RedactedText` | `String` | Required | Redacted text.<br><br>**Constraints**: *Maximum Length*: `32768` | String getRedactedText() | setRedactedText(String redactedText) |
| `ReplacementCount` | `int` | Required | Replacement count.<br><br>**Constraints**: `>= 0`, `<= 128` | int getReplacementCount() | setReplacementCount(int replacementCount) |
| `Reversibility` | `String` | Required, Constant | Reversibility.<br><br>**Value**: `"False"` | String getReversibility() | setReversibility(String reversibility) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` | String getSource() | setSource(String source) |
| `Types` | [`List<TypeEnum>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/type.md) | Required | Types.<br><br>**Constraints**: *Maximum Items*: `7` | List<TypeEnum> getTypes() | setTypes(List<TypeEnum> types) |


# Example

```java
import java.util.Arrays;
import java.util.LinkedHashMap;
import m18000.m0.m0.m127.models.DocumentRedaction;
import m18000.m0.m0.m127.models.TypeEnum;

DocumentRedaction documentRedaction = new DocumentRedaction.Builder(
    new LinkedHashMap<String, Integer>() {{
        put("key0", 128);
        put("key1", 1);
        put("key2", 1);
    }},
    "INTERNAL_REVIEW_ONLY_V1",
    Arrays.asList(
        "limitations3"
    ),
    "True",
    "True",
    "HMAC-SHA256 document pseudonymization v1",
    "redacted_text2",
    128,
    "False",
    "synthetic",
    Arrays.asList(
        TypeEnum.ID_LIKE,
        TypeEnum.NAME,
        TypeEnum.ADDRESS
    )
)
.build();
```



