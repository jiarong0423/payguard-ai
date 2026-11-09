# HTTP Validation Error

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationErrorException`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `detail` | [`?(ValidationError[])`](http://localhost:3000/llms-pages/php/models/structures/validation-error.md) | Optional | Detail. | getDetail(): ?array | setDetail(?array detail): void |


# Example

```php
try {
    // make the API call
} catch (HTTPValidationErrorException $exp) {
    echo 'Caught HTTPValidationErrorException:', $exp;
} catch (ApiException $exp) {
    echo 'Caught ApiException:', $exp;
}
```



