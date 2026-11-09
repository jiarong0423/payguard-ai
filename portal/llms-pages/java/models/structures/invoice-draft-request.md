# Invoice Draft Request

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkludm9pY2VEcmFmdFJlcXVlc3Q

InvoiceDraftRequest.


# Class Name

`InvoiceDraftRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Amount` | `String` | Required | Amount.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,9}(?:\.[0-9]{1,2})?$` | String getAmount() | setAmount(String amount) |
| `Currency` | [`CurrencyEnum`](http://localhost:3000/llms-pages/java/models/enumerations/currency.md) | Required | Currency. | CurrencyEnum getCurrency() | setCurrency(CurrencyEnum currency) |
| `Description` | `String` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` | String getDescription() | setDescription(String description) |
| `PayloadDigest` | `String` | Required | Payload digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getPayloadDigest() | setPayloadDigest(String payloadDigest) |
| `ReviewToken` | `String` | Required | Review token.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128` | String getReviewToken() | setReviewToken(String reviewToken) |


# Example

```java
import m18000.m0.m0.m127.models.CurrencyEnum;
import m18000.m0.m0.m127.models.InvoiceDraftRequest;

InvoiceDraftRequest invoiceDraftRequest = new InvoiceDraftRequest.Builder(
    "amount6",
    CurrencyEnum.JPY,
    "description4",
    "payload_digest6",
    "review_token2"
)
.build();
```



