# ApiException

Source: http://localhost:3000/#/java/x-redirect/JTI0aCUyRl9fYWRkaXRpb25hbF9kb2N1bWVudGF0aW9uJTJGVXRpbGl0aWVzJTJGQXBpRXhjZXB0aW9u

This is the base class for all exceptions that represent an error response from the server.

# Constructors

| Name | Description |
|  --- | --- |
| `ApiException(String reason)` | Initialization constructor. |
| <code>ApiException(String reason, [`HttpContext`](http://localhost:3000/llms-pages/java/sdk-infrastructure/http/httpcontext.md) context)</code> | Initialization constructor. |

# Methods

| Name | Description | Return Type |
|  --- | --- | --- |
| `getResponseCode()` | The HTTP Response code from the API request | `int` |
| `getHttpContext()` | The HTTP Context from the API request. | [`HttpContext`](http://localhost:3000/llms-pages/java/sdk-infrastructure/http/httpcontext.md) |



