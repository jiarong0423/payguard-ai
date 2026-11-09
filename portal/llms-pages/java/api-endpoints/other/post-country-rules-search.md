# Post Country Rules Search

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9jb3VudHJ5X3J1bGVzX3NlYXJjaA

Country Rules Search. Local console route POST /api/v1/country-rules/search on synthetic data; advisory only.

```java
CompletableFuture<Object> postCountryRulesSearchAsync(
    final CountryRulesSearchRequest body)
```


# Authentication

This endpoint requires [DemoCsrf](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/getting-started/how-to-get-started/authorization.md) **AND** [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`CountryRulesSearchRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/country-rules-search-request.md) | Body, Required | JSON body for: Country Rules Search. |


# Response Type

**200**: Successful Response

`Object`


# Example Usage

```java
CountryRulesSearchRequest body = new CountryRulesSearchRequest.Builder(
    "example"
)
.build();

otherController.postCountryRulesSearchAsync(body).thenAccept(result -> {
    // TODO success callback handler
    System.out.println(result);
}).exceptionally(exception -> {
    Throwable cause = exception.getCause();

    if (cause instanceof ErrorBodyException) {
        ErrorBodyException errorBodyException = (ErrorBodyException) cause;
        errorBodyException.printStackTrace();
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
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/exceptions/error-body.md) |
| 403 | Origin missing or not allowed, or the CSRF token is wrong (origin_required, origin_rejected, csrf_rejected). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/exceptions/error-body.md) |
| 422 | The request does not match the accepted contract (schema_invalid). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/exceptions/error-body.md) |



