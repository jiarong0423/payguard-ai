# HTTP Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationError`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `detail` | [`List[ValidationError]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/validation-error.md) | Optional | Detail. |


# Example

```python
import jsonpickle

from tradeglotlocalconsole.models.http_validation_error import HTTPValidationError
from tradeglotlocalconsole.models.validation_error import ValidationError

http_validation_error = HTTPValidationError(
    detail=[
        ValidationError(
            loc=[
                'String7',
                'String8',
                'String9'
            ],
            msg='msg2',
            mtype='type4',
            ctx=jsonpickle.decode('{"key1":"val1","key2":"val2"}'),
            input=jsonpickle.decode('{"key1":"val1","key2":"val2"}')
        ),
        ValidationError(
            loc=[
                'String7',
                'String8',
                'String9'
            ],
            msg='msg2',
            mtype='type4',
            ctx=jsonpickle.decode('{"key1":"val1","key2":"val2"}'),
            input=jsonpickle.decode('{"key1":"val1","key2":"val2"}')
        )
    ]
)
```



