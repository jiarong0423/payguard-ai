# Country Rules Check Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkNvdW50cnlSdWxlc0NoZWNrUmVxdWVzdA

Seller and buyer countries plus closed choices; no free text reaches the check.


# Class Name

`CountryRulesCheckRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AccountOpened` | [`AccountOpenedEnum?`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/account-opened.md) | Optional | Account opened.<br><br>**Default**: `AccountOpenedEnum.unknown` |
| `AccountType` | [`AccountTypeEnum?`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/account-type.md) | Optional | Account type.<br><br>**Default**: `AccountTypeEnum.business` |
| `Amount` | [`CountryRulesCheckRequestAmount`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/country-rules-check-request-amount.md) | Optional | This is a container for any-of cases. |
| `BuyerCountry` | [`BuyerCountryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/buyer-country.md) | Required | Buyer country. |
| `Checkout` | [`CheckoutEnum?`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/checkout.md) | Optional | Checkout.<br><br>**Default**: `CheckoutEnum.paypal_account` |
| `Currency` | [`CountryRulesCheckRequestCurrency`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/country-rules-check-request-currency.md) | Optional | This is a container for any-of cases. |
| `GoodsTags` | `List<string>` | Optional | Goods tags.<br><br>**Constraints**: *Maximum Items*: `16` |
| `SellerCountry` | [`SellerCountryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/seller-country.md) | Required | Seller country. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

CountryRulesCheckRequest countryRulesCheckRequest = new CountryRulesCheckRequest
{
    BuyerCountry = BuyerCountryEnum.JP,
    SellerCountry = SellerCountryEnum.US,
    AccountOpened = AccountOpenedEnum.Unknown,
    AccountType = AccountTypeEnum.Business,
    Amount = CountryRulesCheckRequestAmount.FromString("String7"),
    Checkout = CheckoutEnum.PaypalAccount,
    Currency = CountryRulesCheckRequestCurrency.FromString("String5"),
};
```



