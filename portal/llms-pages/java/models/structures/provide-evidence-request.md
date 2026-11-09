# Provide Evidence Request

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlcXVlc3Q

ProvideEvidenceRequest.


# Class Name

`ProvideEvidenceRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CaseRef` | `String` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` | String getCaseRef() | setCaseRef(String caseRef) |
| `ConfirmToken` | [`ProvideEvidenceRequestConfirmToken`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/provide-evidence-request-confirm-token.md) | Optional | This is a container for any-of cases. | ProvideEvidenceRequestConfirmToken getConfirmToken() | setConfirmToken(ProvideEvidenceRequestConfirmToken confirmToken) |
| `DisputeId` | `String` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` | String getDisputeId() | setDisputeId(String disputeId) |
| `Submit` | `Boolean` | Optional | Submit.<br><br>**Default**: `false` | Boolean getSubmit() | setSubmit(Boolean submit) |


# Example

```java
import m18000.m0.m0.m127.models.ProvideEvidenceRequest;
import m18000.m0.m0.m127.models.containers.ProvideEvidenceRequestConfirmToken;

ProvideEvidenceRequest provideEvidenceRequest = new ProvideEvidenceRequest.Builder(
    "case_ref0",
    "dispute_id8"
)
.confirmToken(ProvideEvidenceRequestConfirmToken.fromString(
        "String7"
    ))
.submit(false)
.build();
```



