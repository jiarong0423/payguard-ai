# Webhook Verify Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRldlYmhvb2tWZXJpZnlSZXNwb25zZQ

WebhookVerifyResponse.


# Class Name

`WebhookVerifyResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Event` | [`WebhookEventProjection`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/webhook-event-projection.md) | Required | All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary. | WebhookEventProjection getEvent() | setEvent(WebhookEventProjection event) |
| `ImportedIntoDemo` | `String` | Required, Constant | Imported into demo.<br><br>**Value**: `"False"` | String getImportedIntoDemo() | setImportedIntoDemo(String importedIntoDemo) |
| `PaypalDebugId` | [`WebhookVerifyResponsePaypalDebugId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/webhook-verify-response-paypal-debug-id.md) | Required | This is a container for any-of cases. | WebhookVerifyResponsePaypalDebugId getPaypalDebugId() | setPaypalDebugId(WebhookVerifyResponsePaypalDebugId paypalDebugId) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"paypal_sandbox"` | String getSource() | setSource(String source) |
| `VerificationStatus` | `String` | Required, Constant | Verification status.<br><br>**Value**: `"SUCCESS"` | String getVerificationStatus() | setVerificationStatus(String verificationStatus) |


# Example

```java
import m18000.m0.m0.m127.models.WebhookEventProjection;
import m18000.m0.m0.m127.models.WebhookVerifyResponse;
import m18000.m0.m0.m127.models.containers.WebhookEventProjectionEventType;
import m18000.m0.m0.m127.models.containers.WebhookEventProjectionId;
import m18000.m0.m0.m127.models.containers.WebhookEventProjectionResourceId;
import m18000.m0.m0.m127.models.containers.WebhookEventProjectionResourceStatus;
import m18000.m0.m0.m127.models.containers.WebhookEventProjectionResourceType;
import m18000.m0.m0.m127.models.containers.WebhookVerifyResponsePaypalDebugId;

WebhookVerifyResponse webhookVerifyResponse = new WebhookVerifyResponse.Builder(
    new WebhookEventProjection.Builder(
        WebhookEventProjectionEventType.fromString(
            "String1"
        ),
        WebhookEventProjectionId.fromString(
            "String1"
        ),
        WebhookEventProjectionResourceId.fromString(
            "String7"
        ),
        WebhookEventProjectionResourceStatus.fromString(
            "String9"
        ),
        WebhookEventProjectionResourceType.fromString(
            "String5"
        )
    )
    .build(),
    "False",
    WebhookVerifyResponsePaypalDebugId.fromString(
        "String9"
    ),
    "paypal_sandbox",
    "SUCCESS"
)
.build();
```



