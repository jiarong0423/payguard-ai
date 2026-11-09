# Error Body

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkVycm9yQm9keQ

The error body every refusal uses.


# Class Name

`ErrorBodyException`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `error` | [`Error`](http://localhost:3000/llms-pages/python/models/structures/error.md) | Required | What was refused and why. |


# Example

```python
try:
    # make the API call
except ErrorBodyException as e:
    print(e)
except APIException as e:
    print(e)
```



