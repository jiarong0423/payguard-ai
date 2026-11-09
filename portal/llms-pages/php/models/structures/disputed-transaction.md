# Disputed Transaction

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkRpc3B1dGVkVHJhbnNhY3Rpb24

DisputedTransaction.


# Class Name

`DisputedTransaction`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `grossAmount` | [ProviderMoney](http://localhost:3000/llms-pages/php/models/structures/provider-money.md)\|null | Optional | This is a container for any-of cases. | getGrossAmount(): ?ProviderMoney | setGrossAmount(?ProviderMoney grossAmount): void |
| `sellerProtectionEligible` | bool\|null | Optional | This is a container for any-of cases. | getSellerProtectionEligible(): ?bool | setSellerProtectionEligible(?bool sellerProtectionEligible): void |
| `sellerTransactionId` | `string` | Required | Seller transaction id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9._-]{1,64}$` | getSellerTransactionId(): string | setSellerTransactionId(string sellerTransactionId): void |
| `transactionStatus` | string\|null | Optional | This is a container for any-of cases. | getTransactionStatus(): ?string | setTransactionStatus(?string transactionStatus): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\DisputedTransactionBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\ProviderMoneyBuilder;

$disputedTransaction = DisputedTransactionBuilder::init(
    'seller_transaction_id8'
)
    ->grossAmount(
        ProviderMoneyBuilder::init(
            'currency_code0',
            'value6'
        )->build()
    )
    ->sellerProtectionEligible(
        true
    )
    ->transactionStatus(
        'String3'
    )
    ->build();
```



