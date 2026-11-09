# Transaction

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlRyYW5zYWN0aW9u

Transaction.


# Class Name

`Transaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Amount` | `string` | Required | Amount. |
| `Currency` | `string` | Required | Currency. |
| `OccurredAt` | `string` | Required | Occurred at. |
| `OrderId` | `string` | Required | Order id. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

Transaction transaction = new Transaction
{
    Amount = "amount0",
    Currency = "currency8",
    OccurredAt = "occurred_at2",
    OrderId = "order_id2",
};
```



