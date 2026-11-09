# Error Body

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkVycm9yQm9keQ

The error body every refusal uses.


# Class Name

`ErrorBodyException`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `error` | [`Error`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/error.md) | Required | What was refused and why. |


# Example

```python
try:
    # make the API call
except ErrorBodyException as e:
    print(e)
except APIException as e:
    print(e)
```



