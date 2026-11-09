# Country Rules Check Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkNvdW50cnlSdWxlc0NoZWNrUmVxdWVzdA

Seller and buyer countries plus closed choices; no free text reaches the check.


# Class Name

`CountryRulesCheckRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AccountOpened` | [`*models.AccountOpenedEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/account-opened.md) | Optional | Account opened.<br><br>**Default**: `"unknown"` |
| `AccountType` | [`*models.AccountTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/account-type.md) | Optional | Account type.<br><br>**Default**: `"business"` |
| `Amount` | [`*models.CountryRulesCheckRequestAmount`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/country-rules-check-request-amount.md) | Optional | This is a container for any-of cases. |
| `BuyerCountry` | [`models.BuyerCountryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/buyer-country.md) | Required | Buyer country. |
| `Checkout` | [`*models.CheckoutEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/checkout.md) | Optional | Checkout.<br><br>**Default**: `"paypal_account"` |
| `Currency` | [`*models.CountryRulesCheckRequestCurrency`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/country-rules-check-request-currency.md) | Optional | This is a container for any-of cases. |
| `GoodsTags` | `[]string` | Optional | Goods tags.<br><br>**Constraints**: *Maximum Items*: `16` |
| `SellerCountry` | [`models.SellerCountryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/seller-country.md) | Required | Seller country. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    countryRulesCheckRequest := models.CountryRulesCheckRequest{
        AccountOpened: models.ToPointer(models.AccountOpenedEnum_UNKNOWN),
        AccountType:   models.ToPointer(models.AccountTypeEnum_BUSINESS),
        Amount:        models.ToPointer(models.CountryRulesCheckRequestAmountContainer.FromString("String7")),
        BuyerCountry:  models.BuyerCountryEnum_JP,
        Checkout:      models.ToPointer(models.CheckoutEnum_PAYPALACCOUNT),
        Currency:      models.ToPointer(models.CountryRulesCheckRequestCurrencyContainer.FromString("String5")),
        SellerCountry: models.SellerCountryEnum_US,
    }

}
```



