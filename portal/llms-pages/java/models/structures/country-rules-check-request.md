# Country Rules Check Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkNvdW50cnlSdWxlc0NoZWNrUmVxdWVzdA

Seller and buyer countries plus closed choices; no free text reaches the check.


# Class Name

`CountryRulesCheckRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AccountOpened` | [`AccountOpenedEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/account-opened.md) | Optional | Account opened.<br><br>**Default**: `AccountOpenedEnum.UNKNOWN` | AccountOpenedEnum getAccountOpened() | setAccountOpened(AccountOpenedEnum accountOpened) |
| `AccountType` | [`AccountTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/account-type.md) | Optional | Account type.<br><br>**Default**: `AccountTypeEnum.BUSINESS` | AccountTypeEnum getAccountType() | setAccountType(AccountTypeEnum accountType) |
| `Amount` | [`CountryRulesCheckRequestAmount`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/country-rules-check-request-amount.md) | Optional | This is a container for any-of cases. | CountryRulesCheckRequestAmount getAmount() | setAmount(CountryRulesCheckRequestAmount amount) |
| `BuyerCountry` | [`BuyerCountryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/buyer-country.md) | Required | Buyer country. | BuyerCountryEnum getBuyerCountry() | setBuyerCountry(BuyerCountryEnum buyerCountry) |
| `Checkout` | [`CheckoutEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/checkout.md) | Optional | Checkout.<br><br>**Default**: `CheckoutEnum.PAYPAL_ACCOUNT` | CheckoutEnum getCheckout() | setCheckout(CheckoutEnum checkout) |
| `Currency` | [`CountryRulesCheckRequestCurrency`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/country-rules-check-request-currency.md) | Optional | This is a container for any-of cases. | CountryRulesCheckRequestCurrency getCurrency() | setCurrency(CountryRulesCheckRequestCurrency currency) |
| `GoodsTags` | `List<String>` | Optional | Goods tags.<br><br>**Constraints**: *Maximum Items*: `16` | List<String> getGoodsTags() | setGoodsTags(List<String> goodsTags) |
| `SellerCountry` | [`SellerCountryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/seller-country.md) | Required | Seller country. | SellerCountryEnum getSellerCountry() | setSellerCountry(SellerCountryEnum sellerCountry) |


# Example

```java
import m18000.m0.m0.m127.models.AccountOpenedEnum;
import m18000.m0.m0.m127.models.AccountTypeEnum;
import m18000.m0.m0.m127.models.BuyerCountryEnum;
import m18000.m0.m0.m127.models.CheckoutEnum;
import m18000.m0.m0.m127.models.CountryRulesCheckRequest;
import m18000.m0.m0.m127.models.SellerCountryEnum;
import m18000.m0.m0.m127.models.containers.CountryRulesCheckRequestAmount;
import m18000.m0.m0.m127.models.containers.CountryRulesCheckRequestCurrency;

CountryRulesCheckRequest countryRulesCheckRequest = new CountryRulesCheckRequest.Builder(
    BuyerCountryEnum.JP,
    SellerCountryEnum.US
)
.accountOpened(AccountOpenedEnum.UNKNOWN)
.accountType(AccountTypeEnum.BUSINESS)
.amount(CountryRulesCheckRequestAmount.fromString(
        "String7"
    ))
.checkout(CheckoutEnum.PAYPAL_ACCOUNT)
.currency(CountryRulesCheckRequestCurrency.fromString(
        "String5"
    ))
.build();
```



