# Dispute Evidence Row

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkRpc3B1dGVFdmlkZW5jZVJvdw

DisputeEvidenceRow.


# Class Name

`DisputeEvidenceRow`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Action` | [`DisputeEvidenceRowAction`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/dispute-evidence-row-action.md) | Optional | This is a container for any-of cases. | DisputeEvidenceRowAction getAction() | setAction(DisputeEvidenceRowAction action) |
| `Date` | [`DisputeEvidenceRowDate`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/dispute-evidence-row-date.md) | Optional | This is a container for any-of cases. | DisputeEvidenceRowDate getDate() | setDate(DisputeEvidenceRowDate date) |
| `EvidenceType` | `String` | Required | Evidence type.<br><br>**Constraints**: *Pattern*: `^[A-Z][A-Z0-9_]{0,63}$` | String getEvidenceType() | setEvidenceType(String evidenceType) |
| `Source` | [`Source3Enum`](http://localhost:3000/llms-pages/java/models/enumerations/source-3.md) | Required | Source. | Source3Enum getSource() | setSource(Source3Enum source) |


# Example

```java
import m18000.m0.m0.m127.models.DisputeEvidenceRow;
import m18000.m0.m0.m127.models.Source3Enum;
import m18000.m0.m0.m127.models.containers.DisputeEvidenceRowAction;
import m18000.m0.m0.m127.models.containers.DisputeEvidenceRowDate;

DisputeEvidenceRow disputeEvidenceRow = new DisputeEvidenceRow.Builder(
    "evidence_type8",
    Source3Enum.REQUESTED_FROM_SELLER
)
.action(DisputeEvidenceRowAction.fromString(
        "String7"
    ))
.date(DisputeEvidenceRowDate.fromString(
        "String3"
    ))
.build();
```



