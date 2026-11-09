# HttpClientConfigurationBuilder

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0aCUyRl9fYWRkaXRpb25hbF9kb2N1bWVudGF0aW9uJTJGQ29uZmlndXJhdGlvbiUyRkh0dHBDbGllbnRDb25maWd1cmF0aW9uQnVpbGRlcg

Class to build instances of HttpClientConfiguration.

# Methods

| Name | Description | Return Type |
|  --- | --- | --- |
| <code>Timeout(TimeSpan timeout)</code> | Http client timeout. | `Builder` |
| <code>NumberOfRetries(int numberOfRetries)</code> | Number of times the request is retried. | `Builder` |
| <code>BackoffFactor(int backoffFactor)</code> | Exponential backoff factor for duration between retry calls. | `Builder` |
| <code>RetryInterval(double retryInterval)</code> | The time interval between the endpoint calls. | `Builder` |
| <code>MaximumRetryWaitTime(TimeSpan maximumRetryWaitTime)</code> | The maximum retry wait time. | `Builder` |
| <code>StatusCodesToRetry(IList<int> statusCodesToRetry)</code> | List of Http status codes to invoke retry. | `Builder` |
| <code>RequestMethodsToRetry(IList<HttpMethod> requestMethodsToRetry)</code> | List of Http request methods to invoke retry. | `Builder` |
| <code>ProxyConfiguration([ProxyConfigurationBuilder](http://localhost:3000/llms-pages/net-standard-library/sdk-infrastructure/configuration/proxyconfigurationbuilder.md) proxyConfiguration)</code> | Configures the proxy server settings used for outbound API calls. | `Builder` |
| <code>HttpClientInstance(HttpClient httpClientInstance)</code> | HttpClient instance used to make the HTTP calls | `Builder` |
| `Build()` | Builds a new HttpClientConfiguration object using the set fields. | [`HttpClientConfiguration`](http://localhost:3000/llms-pages/net-standard-library/sdk-infrastructure/configuration/httpclientconfiguration.md) |



