# HTTP Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationErrorException`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `detail` | [`?(ValidationError[])`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/validation-error.md) | Optional | Detail. | getDetail(): ?array | setDetail(?array detail): void |


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



