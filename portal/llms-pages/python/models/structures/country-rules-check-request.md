# Country Rules Check Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkNvdW50cnlSdWxlc0NoZWNrUmVxdWVzdA

Seller and buyer countries plus closed choices; no free text reaches the check.


# Class Name

`CountryRulesCheckRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `account_opened` | [`AccountOpenedEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/account-opened.md) | Optional | Account opened.<br><br>**Default**: `"unknown"` |
| `account_type` | [`AccountTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/account-type.md) | Optional | Account type.<br><br>**Default**: `"business"` |
| `amount` | str \| None | Optional | This is a container for any-of cases. |
| `buyer_country` | [`BuyerCountryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/buyer-country.md) | Required | Buyer country. |
| `checkout` | [`CheckoutEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/checkout.md) | Optional | Checkout.<br><br>**Default**: `"paypal_account"` |
| `currency` | str \| None | Optional | This is a container for any-of cases. |
| `goods_tags` | `List[str]` | Optional | Goods tags.<br><br>**Constraints**: *Maximum Items*: `16` |
| `seller_country` | [`SellerCountryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/seller-country.md) | Required | Seller country. |


# Example

```python
from tradeglotlocalconsole.models.account_opened_enum import AccountOpenedEnum
from tradeglotlocalconsole.models.account_type_enum import AccountTypeEnum
from tradeglotlocalconsole.models.buyer_country_enum import BuyerCountryEnum
from tradeglotlocalconsole.models.checkout_enum import CheckoutEnum
from tradeglotlocalconsole.models.country_rules_check_request import CountryRulesCheckRequest
from tradeglotlocalconsole.models.seller_country_enum import SellerCountryEnum

country_rules_check_request = CountryRulesCheckRequest(
    buyer_country=BuyerCountryEnum.JP,
    seller_country=SellerCountryEnum.US,
    account_opened=AccountOpenedEnum.UNKNOWN,
    account_type=AccountTypeEnum.BUSINESS,
    amount='String7',
    checkout=CheckoutEnum.PAYPAL_ACCOUNT,
    currency='String5'
)
```



