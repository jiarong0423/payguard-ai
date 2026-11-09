# Dispute Amount

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkRpc3B1dGVBbW91bnQ

Dispute amount.


# Class Name

`DisputeAmount`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CurrencyCode` | `String` | Optional | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` | String getCurrencyCode() | setCurrencyCode(String currencyCode) |
| `Value` | `String` | Optional | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` | String getValue() | setValue(String value) |


# Example

```java
import m18000.m0.m0.m127.models.DisputeAmount;

DisputeAmount disputeAmount = new DisputeAmount.Builder()
    .currencyCode("currency_code0")
    .value("value6")
    .build();
```



