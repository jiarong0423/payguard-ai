# Post Country Rules Check

Source: http://localhost:3000/#/go/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9jb3VudHJ5X3J1bGVzX2NoZWNr

Country Rules Check. Local console route POST /api/v1/country-rules/check on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```go
PostCountryRulesCheck(
    ctx context.Context,
    body models.CountryRulesCheckRequest) (
    models.ApiResponse[interface{}],
    error)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`models.CountryRulesCheckRequest`](http://localhost:3000/llms-pages/go/models/structures/country-rules-check-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](http://localhost:3000/llms-pages/go/sdk-infrastructure/utilities/apiresponse.md) instance. The `Data` property of this instance returns the response data which is of type interface{}.


# Example Usage

```go
ctx := context.Background()

body := models.CountryRulesCheckRequest{
    AccountOpened: models.ToPointer(models.AccountOpenedEnum_UNKNOWN),
    AccountType:   models.ToPointer(models.AccountTypeEnum_BUSINESS),
    BuyerCountry:  models.BuyerCountryEnum_AU,
    Checkout:      models.ToPointer(models.CheckoutEnum_PAYPALACCOUNT),
    SellerCountry: models.SellerCountryEnum_AU,
}

apiResponse, err := otherController.PostCountryRulesCheck(ctx, body)
if err != nil {
    switch typedErr := err.(type) {
        case *errors.ErrorBody:
            log.Fatalln("ErrorBodyException: ", typedErr)
        case *errors.HTTPValidationError:
            log.Fatalln("HTTPValidationErrorException: ", typedErr)
        default:
            log.Fatalln(err)
    }
} else {
    // Printing the result and response
    fmt.Println(apiResponse.Data)
    fmt.Println(apiResponse.Response.StatusCode)
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/go/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/go/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/go/models/exceptions/error-body.md) |



