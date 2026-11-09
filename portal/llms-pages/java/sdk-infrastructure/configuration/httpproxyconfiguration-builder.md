# HttpProxyConfiguration.Builder

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0aCUyRl9fYWRkaXRpb25hbF9kb2N1bWVudGF0aW9uJTJGQ29uZmlndXJhdGlvbiUyRkh0dHBQcm94eUNvbmZpZ3VyYXRpb24uQnVpbGRlcg


Class to build instances of [HttpProxyConfiguration](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/sdk-infrastructure/configuration/httpproxyconfiguration.md).

# Constructors

| Name | Description |
|  --- | --- |
| `Builder()` | Default Constructor to initiate builder with default properties. |

# Methods

| Name | Description | Return Type |
|  --- | --- | --- |
| `Builder(String address, int port)` | Constructs HttpProxyConfiguration.Builder with proxy address and port. | `HttpProxyConfiguration.Builder` |
| `auth(String username, String password)` | Sets the username and password for proxy auth. | `HttpProxyConfiguration.Builder` |
| `build()` | Builds a new HttpProxyConfiguration object using the set fields. | [`HttpProxyConfiguration`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/sdk-infrastructure/configuration/httpproxyconfiguration.md) |

## Client Initialization with Proxy Configuration

To configure the SDK to use a proxy server, initialize the proxy configuration during client setup as shown in the Usage Example.

# Usage Example

```java
import m18000.m0.m0.m127.TradeGlotLocalConsoleClient;
import m18000.m0.m0.m127.http.client.HttpProxyConfiguration;

TradeGlotLocalConsoleClient client = new TradeGlotLocalConsoleClient.Builder()
  .httpClientConfig(configBuilder -> configBuilder
      .proxyConfig(new HttpProxyConfiguration.Builder("http://localhost",
          8080).auth("username", "password")))
  .build();
```



