# Configuration Interface

Source: http://localhost:3000/#/java/x-redirect/JTI0aCUyRl9fYWRkaXRpb25hbF9kb2N1bWVudGF0aW9uJTJGQ29uZmlndXJhdGlvbiUyRkNvbmZpZ3VyYXRpb24lMjUyMEludGVyZmFjZQ

This is the interface for client class that holds the configuration getters.

# Methods

| Name | Description | Return Type |
|  --- | --- | --- |
| `getEnvironment()` | Current API environment. | `Environment` |
| `getHttpClientConfig()` | Http Client Configuration instance. | [`ReadonlyHttpClientConfiguration`](http://localhost:3000/llms-pages/java/sdk-infrastructure/configuration/httpclientconfiguration.md) |
| `getBaseUri(Server server)` | Get base URI by current environment. | `String` |
| `getBaseUri()` | Get base URI by current environment. | `String` |



