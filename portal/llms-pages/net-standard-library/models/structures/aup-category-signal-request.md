# Aup Category Signal Request

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVxdWVzdA

AupCategorySignalRequest.


# Class Name

`AupCategorySignalRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` |
| `EvaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

AupCategorySignalRequest aupCategorySignalRequest = new AupCategorySignalRequest
{
    Description = "description0",
    EvaluationId = "evaluation_id4",
};
```



