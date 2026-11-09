# Country Rules Check Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkNvdW50cnlSdWxlc0NoZWNrUmVxdWVzdA

Seller and buyer countries plus closed choices; no free text reaches the check.


# Interface Name

`CountryRulesCheckRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `accountOpened` | [`AccountOpenedEnum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/account-opened.md) | Optional | Account opened.<br><br>**Default**: `AccountOpenedEnum.Unknown` |
| `accountType` | [`AccountTypeEnum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/account-type.md) | Optional | Account type.<br><br>**Default**: `AccountTypeEnum.Business` |
| `amount` | [`CountryRulesCheckRequestAmount \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/country-rules-check-request-amount.md) | Optional | This is a container for any-of cases. |
| `buyerCountry` | [`BuyerCountryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/buyer-country.md) | Required | Buyer country. |
| `checkout` | [`CheckoutEnum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/checkout.md) | Optional | Checkout.<br><br>**Default**: `CheckoutEnum.PaypalAccount` |
| `currency` | [`CountryRulesCheckRequestCurrency \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/country-rules-check-request-currency.md) | Optional | This is a container for any-of cases. |
| `goodsTags` | `string[] \| undefined` | Optional | Goods tags.<br><br>**Constraints**: *Maximum Items*: `16` |
| `sellerCountry` | [`SellerCountryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/seller-country.md) | Required | Seller country. |


# Example

```ts
import {
  AccountOpenedEnum,
  AccountTypeEnum,
  BuyerCountryEnum,
  CheckoutEnum,
  CountryRulesCheckRequest,
  SellerCountryEnum,
} from 'tradeglot-local-consolelib';

const countryRulesCheckRequest: CountryRulesCheckRequest = {
  buyerCountry: BuyerCountryEnum.JP,
  sellerCountry: SellerCountryEnum.US,
  accountOpened: AccountOpenedEnum.Unknown,
  accountType: AccountTypeEnum.Business,
  amount: 'String7',
  checkout: CheckoutEnum.PaypalAccount,
  currency: 'String5',
};
```



