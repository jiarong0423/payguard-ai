# Product Reference Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlByb2R1Y3RSZWZlcmVuY2VSZXF1ZXN0

ProductReferenceRequest.


# Class Name

`ProductReferenceRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` |
| `EvaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

ProductReferenceRequest productReferenceRequest = new ProductReferenceRequest
{
    Description = "description8",
    EvaluationId = "evaluation_id2",
};
```



