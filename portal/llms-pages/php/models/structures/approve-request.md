# Approve Request

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkFwcHJvdmVSZXF1ZXN0

ApproveRequest.


# Class Name

`ApproveRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `draftDigest` | `string` | Required | Draft digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getDraftDigest(): string | setDraftDigest(string draftDigest): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ApproveRequestBuilder;

$approveRequest = ApproveRequestBuilder::init(
    'draft_digest6'
)->build();
```



