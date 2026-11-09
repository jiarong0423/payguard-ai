# Disputed Transaction Gross Amount

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkRpc3B1dGVkVHJhbnNhY3Rpb25Hcm9zc0Ftb3VudA


# Class Name

`DisputedTransactionGrossAmount`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`ProviderMoney`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/provider-money.md) | DisputedTransactionGrossAmount.FromProviderMoney(ProviderMoney providerMoney) |


# ProviderMoney

## Initialization Code

### Example

```csharp
DisputedTransactionGrossAmount value = DisputedTransactionGrossAmount.FromProviderMoney(
    new ProviderMoney
    {
        CurrencyCode = "currency_code0",
        MValue = "value6",
    }
);
```



