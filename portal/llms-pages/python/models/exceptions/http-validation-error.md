# HTTP Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationErrorException`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `detail` | [`List[ValidationError]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/validation-error.md) | Optional | Detail. |


# Example

```python
try:
    # make the API call
except HTTPValidationErrorException as e:
    print(e)
except APIException as e:
    print(e)
```



