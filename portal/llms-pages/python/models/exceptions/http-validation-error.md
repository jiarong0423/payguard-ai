# HTTP Validation Error

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationErrorException`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `detail` | [`List[ValidationError]`](http://localhost:3000/llms-pages/python/models/structures/validation-error.md) | Optional | Detail. |


# Example

```python
try:
    # make the API call
except HTTPValidationErrorException as e:
    print(e)
except APIException as e:
    print(e)
```



