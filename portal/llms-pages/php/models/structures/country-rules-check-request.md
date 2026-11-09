# Country Rules Check Request

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkNvdW50cnlSdWxlc0NoZWNrUmVxdWVzdA

Seller and buyer countries plus closed choices; no free text reaches the check.


# Class Name

`CountryRulesCheckRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `accountOpened` | [`?string(AccountOpenedEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/account-opened.md) | Optional | Account opened.<br><br>**Default**: `AccountOpenedEnum::UNKNOWN` | getAccountOpened(): ?string | setAccountOpened(?string accountOpened): void |
| `accountType` | [`?string(AccountTypeEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/account-type.md) | Optional | Account type.<br><br>**Default**: `AccountTypeEnum::BUSINESS` | getAccountType(): ?string | setAccountType(?string accountType): void |
| `amount` | string\|null | Optional | This is a container for any-of cases. | getAmount(): ?string | setAmount(?string amount): void |
| `buyerCountry` | [`string(BuyerCountryEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/buyer-country.md) | Required | Buyer country. | getBuyerCountry(): string | setBuyerCountry(string buyerCountry): void |
| `checkout` | [`?string(CheckoutEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/checkout.md) | Optional | Checkout.<br><br>**Default**: `CheckoutEnum::PAYPAL_ACCOUNT` | getCheckout(): ?string | setCheckout(?string checkout): void |
| `currency` | string\|null | Optional | This is a container for any-of cases. | getCurrency(): ?string | setCurrency(?string currency): void |
| `goodsTags` | `?(string[])` | Optional | Goods tags.<br><br>**Constraints**: *Maximum Items*: `16` | getGoodsTags(): ?array | setGoodsTags(?array goodsTags): void |
| `sellerCountry` | [`string(SellerCountryEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/seller-country.md) | Required | Seller country. | getSellerCountry(): string | setSellerCountry(string sellerCountry): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\CountryRulesCheckRequestBuilder;
use TradeGlotLocalConsoleLib\Models\BuyerCountryEnum;
use TradeGlotLocalConsoleLib\Models\SellerCountryEnum;
use TradeGlotLocalConsoleLib\Models\AccountOpenedEnum;
use TradeGlotLocalConsoleLib\Models\AccountTypeEnum;
use TradeGlotLocalConsoleLib\Models\CheckoutEnum;

$countryRulesCheckRequest = CountryRulesCheckRequestBuilder::init(
    BuyerCountryEnum::JP,
    SellerCountryEnum::US
)
    ->accountOpened(AccountOpenedEnum::UNKNOWN)
    ->accountType(AccountTypeEnum::BUSINESS)
    ->amount(
        'String7'
    )
    ->checkout(CheckoutEnum::PAYPAL_ACCOUNT)
    ->currency(
        'String5'
    )
    ->build();
```



