# Invoice Review Response

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkludm9pY2VSZXZpZXdSZXNwb25zZQ

InvoiceReviewResponse.


# Class Name

`InvoiceReviewResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Action` | `String` | Required, Constant | Action.<br><br>**Value**: `"create_sandbox_invoice_draft"` | String getAction() | setAction(String action) |
| `AdvisoryOnly` | `String` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` | String getAdvisoryOnly() | setAdvisoryOnly(String advisoryOnly) |
| `AuthenticatedActor` | `String` | Required, Constant | Authenticated actor.<br><br>**Value**: `"False"` | String getAuthenticatedActor() | setAuthenticatedActor(String authenticatedActor) |
| `ExpiresAt` | `String` | Required | Expires at. | String getExpiresAt() | setExpiresAt(String expiresAt) |
| `Limitations` | `List<String>` | Required | Limitations. | List<String> getLimitations() | setLimitations(List<String> limitations) |
| `PayloadDigest` | `String` | Required | Payload digest. | String getPayloadDigest() | setPayloadDigest(String payloadDigest) |
| `PolicyStatus` | `String` | Required, Constant | Policy status.<br><br>**Value**: `"manual_review"` | String getPolicyStatus() | setPolicyStatus(String policyStatus) |
| `ReviewToken` | `String` | Required | Review token. | String getReviewToken() | setReviewToken(String reviewToken) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` | String getSource() | setSource(String source) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.InvoiceReviewResponse;

InvoiceReviewResponse invoiceReviewResponse = new InvoiceReviewResponse.Builder(
    "create_sandbox_invoice_draft",
    "True",
    "False",
    "expires_at8",
    Arrays.asList(
        "limitations5",
        "limitations6"
    ),
    "payload_digest8",
    "manual_review",
    "review_token6",
    "synthetic"
)
.build();
```



