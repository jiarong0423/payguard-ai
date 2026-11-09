# HttpCallback Interface

Source: http://localhost:3000/#/java/x-redirect/JTI0aCUyRl9fYWRkaXRpb25hbF9kb2N1bWVudGF0aW9uJTJGSFRUUCUyRkh0dHBDYWxsYmFjayUyNTIwSW50ZXJmYWNl

Callback to be called before and after the HTTP call for an endpoint is made.

# Methods

| Name | Description | Return Type |
|  --- | --- | --- |
| <code>onBeforeRequest([`HttpRequest`](http://localhost:3000/llms-pages/java/sdk-infrastructure/http/httprequest.md) request)</code> | Callback called just before the HTTP request is sent. | `void` |
| <code>onAfterResponse([`HttpContext`](http://localhost:3000/llms-pages/java/sdk-infrastructure/http/httpcontext.md) context)</code> | Callback called just after the HTTP response is received. | `void` |



