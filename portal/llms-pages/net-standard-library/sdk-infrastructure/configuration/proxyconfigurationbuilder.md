# ProxyConfigurationBuilder

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0aCUyRl9fYWRkaXRpb25hbF9kb2N1bWVudGF0aW9uJTJGQ29uZmlndXJhdGlvbiUyRlByb3h5Q29uZmlndXJhdGlvbkJ1aWxkZXI


Represents the proxy server configurations for API calls. Start building by using `new ProxyConfigurationBuilder("http://your.proxy.host")`.

# Builder Methods

| Name | Description | Return Type |
|  --- | --- | --- |
| <code>Port(int port)</code> | Sets the port used to connect to the proxy server. Default is `8080`. | <code>Builder</code> |
| <code>Auth(string user, string pass)</code> | Sets both username and password in a single method. | <code>Builder</code> |
| <code>Tunnel(bool tunnel)</code> | Enables or disables HTTP tunneling through the proxy server. | <code>Builder</code> |

## Client Initialization with Proxy Configuration

To configure the SDK to use a proxy server, initialize the proxy configuration during client setup as shown in the Usage Example.

# Usage Example

```csharp
using TradeGlotLocalConsole.Standard;
using TradeGlotLocalConsole.Standard.Http.Client.Proxy;

namespace ConsoleApp;

var client = new TradeGlotLocalConsoleClient.Builder()
.HttpClientConfig(config => config
    .Proxy(new ProxyConfigurationBuilder("http://localhost")
            .Port(8080)
            .Tunnel(false)
            .Auth("user", "pass")
    )
)
.Build();
```



