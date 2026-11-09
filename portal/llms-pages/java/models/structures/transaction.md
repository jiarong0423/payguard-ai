# Transaction

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlRyYW5zYWN0aW9u

Transaction.


# Class Name

`Transaction`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Amount` | `String` | Required | Amount. | String getAmount() | setAmount(String amount) |
| `Currency` | `String` | Required | Currency. | String getCurrency() | setCurrency(String currency) |
| `OccurredAt` | `String` | Required | Occurred at. | String getOccurredAt() | setOccurredAt(String occurredAt) |
| `OrderId` | `String` | Required | Order id. | String getOrderId() | setOrderId(String orderId) |


# Example

```java
import m18000.m0.m0.m127.models.Transaction;

Transaction transaction = new Transaction.Builder(
    "amount0",
    "currency8",
    "occurred_at2",
    "order_id2"
)
.build();
```



