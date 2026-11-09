# Error Body

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkVycm9yQm9keQ

The error body every refusal uses.


# Class Name

`ErrorBodyException`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `error` | [`Error`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/error.md) | Required | What was refused and why. | getError(): Error | setError(Error error): void |


# Example

```php
try {
    // make the API call
} catch (ErrorBodyException $exp) {
    echo 'Caught ErrorBodyException:', $exp;
} catch (ApiException $exp) {
    echo 'Caught ApiException:', $exp;
}
```



