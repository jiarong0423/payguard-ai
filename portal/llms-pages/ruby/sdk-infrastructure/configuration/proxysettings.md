# ProxySettings

Source: http://localhost:3000/#/ruby/x-redirect/JTI0aCUyRl9fYWRkaXRpb25hbF9kb2N1bWVudGF0aW9uJTJGQ29uZmlndXJhdGlvbiUyRlByb3h5U2V0dGluZ3M


Represents the proxy server configurations for API calls.

# Properties

| Name | Type | Tag | Description |
|  --- | --- | --- | --- |
| address | `String` | required | The proxy server URL. |
| port | `Integer` | optional | The port to connect to the proxy server. |
| username | `String` | optional | Username for proxy authentication. |
| password | `String` | optional | Password for proxy authentication. |

# Usage Example

```ruby
require 'trade_glot_local_console'
include TradeGlotLocalConsole


client = TradeGlotLocalConsole::Client.new(
  proxy_settings: ProxySettings.new(
    address: "http://localhost",
    port: 8888,
    username: 'user',
    password: 'pass'
  )
)
```



