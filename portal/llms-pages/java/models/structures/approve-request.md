# Approve Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkFwcHJvdmVSZXF1ZXN0

ApproveRequest.


# Class Name

`ApproveRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `DraftDigest` | `String` | Required | Draft digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getDraftDigest() | setDraftDigest(String draftDigest) |


# Example

```java
import m18000.m0.m0.m127.models.ApproveRequest;

ApproveRequest approveRequest = new ApproveRequest.Builder(
    "draft_digest6"
)
.build();
```



