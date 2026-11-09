# Disputed Transaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkRpc3B1dGVkVHJhbnNhY3Rpb24

DisputedTransaction.


# Class Name

`DisputedTransaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `GrossAmount` | [`*models.DisputedTransactionGrossAmount`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/disputed-transaction-gross-amount.md) | Optional | This is a container for any-of cases. |
| `SellerProtectionEligible` | [`*models.DisputedTransactionSellerProtectionEligible`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/disputed-transaction-seller-protection-eligible.md) | Optional | This is a container for any-of cases. |
| `SellerTransactionId` | `string` | Required | Seller transaction id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9._-]{1,64}$` |
| `TransactionStatus` | [`*models.DisputedTransactionTransactionStatus`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/disputed-transaction-transaction-status.md) | Optional | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    disputedTransaction := models.DisputedTransaction{
        GrossAmount:              models.ToPointer(models.DisputedTransactionGrossAmountContainer.FromProviderMoney(models.ProviderMoney{
            CurrencyCode:         "currency_code0",
            Value:                "value6",
        })),
        SellerProtectionEligible: models.ToPointer(models.DisputedTransactionSellerProtectionEligibleContainer.FromBoolean(true)),
        SellerTransactionId:      "seller_transaction_id8",
        TransactionStatus:        models.ToPointer(models.DisputedTransactionTransactionStatusContainer.FromString("String3")),
    }

}
```



