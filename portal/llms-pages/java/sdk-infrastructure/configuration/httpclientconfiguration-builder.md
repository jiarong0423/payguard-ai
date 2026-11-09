# HttpClientConfiguration.Builder

Source: http://localhost:3000/#/java/x-redirect/JTI0aCUyRl9fYWRkaXRpb25hbF9kb2N1bWVudGF0aW9uJTJGQ29uZmlndXJhdGlvbiUyRkh0dHBDbGllbnRDb25maWd1cmF0aW9uLkJ1aWxkZXI

Class to build instances of [HttpClientConfiguration](http://localhost:3000/llms-pages/java/sdk-infrastructure/configuration/httpclientconfiguration.md).

# Constructors

| Name | Description |
|  --- | --- |
| `Builder()` | Default Constructor to initiate builder with default properties. |

# Methods

| Name | Description | Return Type |
|  --- | --- | --- |
| `timeout(long timeout)` | Sets the timeout in seconds to use for making http requests. | `HttpClientConfiguration.Builder` |
| `numberOfRetries(int numberOfRetries)` | Sets the number of retries to make. | `HttpClientConfiguration.Builder` |
| `backOffFactor(int backOffFactor)` | Sets to use in calculation of wait time for next request in case of failure. | `HttpClientConfiguration.Builder` |
| `retryInterval(long retryInterval)` | Sets to use in calculation of wait time for next request in case of failure. | `HttpClientConfiguration.Builder` |
| `httpStatusCodesToRetry(Set<Integer> httpStatusCodesToRetry)` | Sets http status codes to retry against. | `HttpClientConfiguration.Builder` |
| `httpMethodsToRetry(Set<HttpMethod> httpMethodsToRetry)` | Sets http methods to retry against. | `HttpClientConfiguration.Builder` |
| `maximumRetryWaitTime(long maximumRetryWaitTime)` | Sets the maximum wait time for overall retrying requests. | `HttpClientConfiguration.Builder` |
| `shouldRetryOnTimeout(boolean shouldRetryOnTimeout)` | Sets whether to retry on request timeout. | `HttpClientConfiguration.Builder` |
| `httpClientInstance(okhttp3.OkHttpClient httpClientInstance)` | Sets the okhttpclient instance used to make the http calls. | `HttpClientConfiguration.Builder` |
| `httpClientInstance(okhttp3.OkHttpClient httpClientInstance, boolean overrideHttpClientConfigurations)` | Sets the okhttpclient instance used to make the http calls and an option to Allow the SDK to override HTTP client instance's settings used for features like retries, timeouts etc. | `HttpClientConfiguration.Builder` |
| <code>proxyConfig([HttpProxyConfiguration.Builder](http://localhost:3000/llms-pages/java/sdk-infrastructure/configuration/httpproxyconfiguration-builder.md) proxyBuilder)</code> | Sets the proxy configuration for the underlying HTTP client. | `HttpClientConfiguration.Builder` |
| `build()` | Builds a new HttpClientConfiguration object using the set fields. | [`HttpClientConfiguration`](http://localhost:3000/llms-pages/java/sdk-infrastructure/configuration/httpclientconfiguration.md) |



