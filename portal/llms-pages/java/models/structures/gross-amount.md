# Gross Amount

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkdyb3NzQW1vdW50

Gross amount.


# Class Name

`GrossAmount`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CurrencyCode` | `String` | Optional | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` | String getCurrencyCode() | setCurrencyCode(String currencyCode) |
| `Value` | `String` | Optional | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` | String getValue() | setValue(String value) |


# Example

```java
import m18000.m0.m0.m127.models.GrossAmount;

GrossAmount grossAmount = new GrossAmount.Builder()
    .currencyCode("currency_code6")
    .value("value2")
    .build();
```



