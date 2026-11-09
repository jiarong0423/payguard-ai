# Disputed Transaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkRpc3B1dGVkVHJhbnNhY3Rpb24

DisputedTransaction.


# Class Name

`DisputedTransaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `GrossAmount` | [`DisputedTransactionGrossAmount`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/disputed-transaction-gross-amount.md) | Optional | This is a container for any-of cases. |
| `SellerProtectionEligible` | [`DisputedTransactionSellerProtectionEligible`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/disputed-transaction-seller-protection-eligible.md) | Optional | This is a container for any-of cases. |
| `SellerTransactionId` | `string` | Required | Seller transaction id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9._-]{1,64}$` |
| `TransactionStatus` | [`DisputedTransactionTransactionStatus`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/disputed-transaction-transaction-status.md) | Optional | This is a container for any-of cases. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

DisputedTransaction disputedTransaction = new DisputedTransaction
{
    SellerTransactionId = "seller_transaction_id8",
    GrossAmount = DisputedTransactionGrossAmount.FromProviderMoney(
        new ProviderMoney
        {
            CurrencyCode = "currency_code0",
            MValue = "value6",
        }
    ),
    SellerProtectionEligible = DisputedTransactionSellerProtectionEligible.FromBoolean(true),
    TransactionStatus = DisputedTransactionTransactionStatus.FromString("String3"),
};
```



