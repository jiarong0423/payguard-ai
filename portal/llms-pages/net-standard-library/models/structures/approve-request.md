# Approve Request

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkFwcHJvdmVSZXF1ZXN0

ApproveRequest.


# Class Name

`ApproveRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `DraftDigest` | `string` | Required | Draft digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

ApproveRequest approveRequest = new ApproveRequest
{
    DraftDigest = "draft_digest6",
};
```



