# Add Tracking Request

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkFkZFRyYWNraW5nUmVxdWVzdA

AddTrackingRequest.


# Class Name

`AddTrackingRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CaseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `ConfirmToken` | [`AddTrackingRequestConfirmToken`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/add-tracking-request-confirm-token.md) | Optional | This is a container for any-of cases. |
| `DisputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `Submit` | `bool?` | Optional | Submit.<br><br>**Default**: `false` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

AddTrackingRequest addTrackingRequest = new AddTrackingRequest
{
    CaseRef = "case_ref4",
    DisputeId = "dispute_id2",
    ConfirmToken = AddTrackingRequestConfirmToken.FromString("String1"),
    Submit = false,
};
```



