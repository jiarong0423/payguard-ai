# Post Paypal Webhooks Verify

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX3dlYmhvb2tzX3ZlcmlmeQ

Verify Webhook. Local console route POST /api/v1/paypal/webhooks/verify on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostPaypalWebhooksVerifyAsync()
```


# Response Type

**200**: Successful Response

[`Task<Models.WebhookVerifyResponse>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/webhook-verify-response.md)


# Example Usage

```csharp
try
{
    WebhookVerifyResponse result = await paypalController.PostPaypalWebhooksVerifyAsync();
}
catch (ApiException e)
{
    Console.WriteLine(e.Message);
    if (e is ErrorBodyException)
    {
       // TODO: Handle ErrorBodyException exception here
    }
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/net-standard-library/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/net-standard-library/models/exceptions/error-body.md) |



