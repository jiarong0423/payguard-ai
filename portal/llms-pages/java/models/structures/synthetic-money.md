# Synthetic Money

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlN5bnRoZXRpY01vbmV5

Same shape as the PayPal Disputes `dispute_amount` (ProviderMoney below); values are synthetic.


# Class Name

`SyntheticMoney`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CurrencyCode` | `String` | Required | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` | String getCurrencyCode() | setCurrencyCode(String currencyCode) |
| `Value` | `String` | Required | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` | String getValue() | setValue(String value) |


# Example

```java
import m18000.m0.m0.m127.models.SyntheticMoney;

SyntheticMoney syntheticMoney = new SyntheticMoney.Builder(
    "currency_code8",
    "value4"
)
.build();
```



