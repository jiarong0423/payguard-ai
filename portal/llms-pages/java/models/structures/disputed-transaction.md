# Disputed Transaction

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkRpc3B1dGVkVHJhbnNhY3Rpb24

DisputedTransaction.


# Class Name

`DisputedTransaction`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `GrossAmount` | [`DisputedTransactionGrossAmount`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/disputed-transaction-gross-amount.md) | Optional | This is a container for any-of cases. | DisputedTransactionGrossAmount getGrossAmount() | setGrossAmount(DisputedTransactionGrossAmount grossAmount) |
| `SellerProtectionEligible` | [`DisputedTransactionSellerProtectionEligible`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/disputed-transaction-seller-protection-eligible.md) | Optional | This is a container for any-of cases. | DisputedTransactionSellerProtectionEligible getSellerProtectionEligible() | setSellerProtectionEligible(DisputedTransactionSellerProtectionEligible sellerProtectionEligible) |
| `SellerTransactionId` | `String` | Required | Seller transaction id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9._-]{1,64}$` | String getSellerTransactionId() | setSellerTransactionId(String sellerTransactionId) |
| `TransactionStatus` | [`DisputedTransactionTransactionStatus`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/disputed-transaction-transaction-status.md) | Optional | This is a container for any-of cases. | DisputedTransactionTransactionStatus getTransactionStatus() | setTransactionStatus(DisputedTransactionTransactionStatus transactionStatus) |


# Example

```java
import m18000.m0.m0.m127.models.DisputedTransaction;
import m18000.m0.m0.m127.models.ProviderMoney;
import m18000.m0.m0.m127.models.containers.DisputedTransactionGrossAmount;
import m18000.m0.m0.m127.models.containers.DisputedTransactionSellerProtectionEligible;
import m18000.m0.m0.m127.models.containers.DisputedTransactionTransactionStatus;

DisputedTransaction disputedTransaction = new DisputedTransaction.Builder(
    "seller_transaction_id8"
)
.grossAmount(DisputedTransactionGrossAmount.fromProviderMoney(
        new ProviderMoney.Builder(
            "currency_code0",
            "value6"
        )
        .build()
    ))
.sellerProtectionEligible(DisputedTransactionSellerProtectionEligible.fromBoolean(
        true
    ))
.transactionStatus(DisputedTransactionTransactionStatus.fromString(
        "String3"
    ))
.build();
```



