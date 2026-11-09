# Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlZhbGlkYXRpb25FcnJvcg

ValidationError.


# Class Name

`ValidationError`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `ctx` | `Any` | Optional | Ctx. |
| `input` | `Any` | Optional | Input. |
| `loc` | List[str \| int] | Required | This is List of a container for any-of cases. |
| `msg` | `str` | Required | Msg. |
| `mtype` | `str` | Required | Type. |


# Example

```python
import jsonpickle

from tradeglotlocalconsole.models.validation_error import ValidationError

validation_error = ValidationError(
    loc=[
        'String9',
        'String0',
        'String1'
    ],
    msg='msg4',
    mtype='type2',
    ctx=jsonpickle.decode('{"key1":"val1","key2":"val2"}'),
    input=jsonpickle.decode('{"key1":"val1","key2":"val2"}')
)
```



