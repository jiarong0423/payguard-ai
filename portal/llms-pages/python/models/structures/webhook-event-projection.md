# Webhook Event Projection

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRldlYmhvb2tFdmVudFByb2plY3Rpb24

All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary.


# Class Name

`WebhookEventProjection`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `event_type` | str | Required | This is a container for any-of cases. |
| `id` | str | Required | This is a container for any-of cases. |
| `resource_id` | str | Required | This is a container for any-of cases. |
| `resource_status` | str | Required | This is a container for any-of cases. |
| `resource_type` | str | Required | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.webhook_event_projection import WebhookEventProjection

webhook_event_projection = WebhookEventProjection(
    event_type='String7',
    id='String7',
    resource_id='String3',
    resource_status='String9',
    resource_type='String1'
)
```



