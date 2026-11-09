# Post Country Rules Check

Source: http://localhost:3000/#/java/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9jb3VudHJ5X3J1bGVzX2NoZWNr

Country Rules Check. Local console route POST /api/v1/country-rules/check on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```java
CompletableFuture<Object> postCountryRulesCheckAsync(
    final CountryRulesCheckRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`CountryRulesCheckRequest`](http://localhost:3000/llms-pages/java/models/structures/country-rules-check-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

`Object`


# Example Usage

```java
CountryRulesCheckRequest body = new CountryRulesCheckRequest.Builder(
    BuyerCountryEnum.AU,
    SellerCountryEnum.AU
)
.accountOpened(AccountOpenedEnum.UNKNOWN)
.accountType(AccountTypeEnum.BUSINESS)
.checkout(CheckoutEnum.PAYPAL_ACCOUNT)
.build();

otherController.postCountryRulesCheckAsync(body).thenAccept(result -> {
    // TODO success callback handler
    System.out.println(result);
}).exceptionally(exception -> {
    Throwable cause = exception.getCause();

    if (cause instanceof ErrorBodyException) {
        ErrorBodyException errorBodyException = (ErrorBodyException) cause;
        errorBodyException.printStackTrace();
    } else if (cause instanceof HTTPValidationErrorException) {
        HTTPValidationErrorException hTTPValidationErrorException = (HTTPValidationErrorException) cause;
        hTTPValidationErrorException.printStackTrace();
    } else {
        // fallback for unexpected errors
        exception.printStackTrace();
    }

    return null;
});
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/java/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/java/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/java/models/exceptions/error-body.md) |



