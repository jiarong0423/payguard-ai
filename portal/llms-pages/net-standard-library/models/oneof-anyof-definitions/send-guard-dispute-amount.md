# Send Guard Dispute Amount

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlNlbmRHdWFyZERpc3B1dGVBbW91bnQ


# Class Name

`SendGuardDisputeAmount`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`ProviderMoney`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/provider-money.md) | SendGuardDisputeAmount.FromProviderMoney(ProviderMoney providerMoney) |


# ProviderMoney

## Initialization Code

### Example

```csharp
SendGuardDisputeAmount value = SendGuardDisputeAmount.FromProviderMoney(
    new ProviderMoney
    {
        CurrencyCode = "currency_code0",
        MValue = "value6",
    }
);
```



