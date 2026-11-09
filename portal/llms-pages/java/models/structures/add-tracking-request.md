# Add Tracking Request

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkFkZFRyYWNraW5nUmVxdWVzdA

AddTrackingRequest.


# Class Name

`AddTrackingRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CaseRef` | `String` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` | String getCaseRef() | setCaseRef(String caseRef) |
| `ConfirmToken` | [`AddTrackingRequestConfirmToken`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/add-tracking-request-confirm-token.md) | Optional | This is a container for any-of cases. | AddTrackingRequestConfirmToken getConfirmToken() | setConfirmToken(AddTrackingRequestConfirmToken confirmToken) |
| `DisputeId` | `String` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` | String getDisputeId() | setDisputeId(String disputeId) |
| `Submit` | `Boolean` | Optional | Submit.<br><br>**Default**: `false` | Boolean getSubmit() | setSubmit(Boolean submit) |


# Example

```java
import m18000.m0.m0.m127.models.AddTrackingRequest;
import m18000.m0.m0.m127.models.containers.AddTrackingRequestConfirmToken;

AddTrackingRequest addTrackingRequest = new AddTrackingRequest.Builder(
    "case_ref4",
    "dispute_id2"
)
.confirmToken(AddTrackingRequestConfirmToken.fromString(
        "String1"
    ))
.submit(false)
.build();
```



