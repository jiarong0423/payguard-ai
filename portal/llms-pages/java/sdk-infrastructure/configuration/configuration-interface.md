# Configuration Interface

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0aCUyRl9fYWRkaXRpb25hbF9kb2N1bWVudGF0aW9uJTJGQ29uZmlndXJhdGlvbiUyRkNvbmZpZ3VyYXRpb24lMjUyMEludGVyZmFjZQ

This is the interface for client class that holds the configuration getters.

# Methods

| Name | Description | Return Type |
|  --- | --- | --- |
| `getEnvironment()` | Current API environment. | `Environment` |
| `getHttpClientConfig()` | Http Client Configuration instance. | [`ReadonlyHttpClientConfiguration`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/sdk-infrastructure/configuration/httpclientconfiguration.md) |
| `getBaseUri(Server server)` | Get base URI by current environment. | `String` |
| `getBaseUri()` | Get base URI by current environment. | `String` |



