# Webhook Event Projection

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRldlYmhvb2tFdmVudFByb2plY3Rpb24

All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary.


# Class Name

`WebhookEventProjection`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `event_type` | String | Required | This is a container for any-of cases. |
| `id` | String | Required | This is a container for any-of cases. |
| `resource_id` | String | Required | This is a container for any-of cases. |
| `resource_status` | String | Required | This is a container for any-of cases. |
| `resource_type` | String | Required | This is a container for any-of cases. |


# Example

```ruby
webhook_event_projection = WebhookEventProjection.new(
  'String7',
  'String7',
  'String3',
  'String9',
  'String1'
)
```



