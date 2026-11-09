# Approve Request

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkFwcHJvdmVSZXF1ZXN0

ApproveRequest.


# Class Name

`ApproveRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `draft_digest` | `String` | Required | Draft digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |


# Example

```ruby
approve_request = ApproveRequest.new(
  'draft_digest6'
)
```



