# Country Rules Check Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkNvdW50cnlSdWxlc0NoZWNrUmVxdWVzdA

Seller and buyer countries plus closed choices; no free text reaches the check.


# Class Name

`CountryRulesCheckRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `account_opened` | [`AccountOpenedEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/account-opened.md) | Optional | Account opened.<br><br>**Default**: `AccountOpenedEnum::UNKNOWN` |
| `account_type` | [`AccountTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/account-type.md) | Optional | Account type.<br><br>**Default**: `AccountTypeEnum::BUSINESS` |
| `amount` | String \| nil | Optional | This is a container for any-of cases. |
| `buyer_country` | [`BuyerCountryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/buyer-country.md) | Required | Buyer country. |
| `checkout` | [`CheckoutEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/checkout.md) | Optional | Checkout.<br><br>**Default**: `CheckoutEnum::PAYPAL_ACCOUNT` |
| `currency` | String \| nil | Optional | This is a container for any-of cases. |
| `goods_tags` | `Array[String]` | Optional | Goods tags.<br><br>**Constraints**: *Maximum Items*: `16` |
| `seller_country` | [`SellerCountryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/seller-country.md) | Required | Seller country. |


# Example

```ruby
country_rules_check_request = CountryRulesCheckRequest.new(
  BuyerCountryEnum::JP,
  SellerCountryEnum::US,
  AccountOpenedEnum::UNKNOWN,
  AccountTypeEnum::BUSINESS,
  'String7',
  CheckoutEnum::PAYPAL_ACCOUNT,
  'String5',
  []
)
```



