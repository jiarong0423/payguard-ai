# ApiResponse

Source: http://localhost:3000/#/go/x-redirect/JTI0aCUyRl9fYWRkaXRpb25hbF9kb2N1bWVudGF0aW9uJTJGVXRpbGl0aWVzJTJGQXBpUmVzcG9uc2U


Represents the result of an API call, including response metadata and the returned data of type `T`.

# Properties

| Name | Type | Description |
|  --- | --- | --- |
| `Response` | `*http.Response` | Returns the complete response information. |
| `Data` | `T` | Returns the response data. |

# Usage Example

```go
package main

import (
    "fmt"
    "log"
)

func main() {
    apiResponse, err := client.ExampleController().GetExampleType(ctx, body)

    if err != nil {
        log.Fatalln("Error: ", err)
    } else {
        fmt.Println("Success! Result: ", apiResponse.Data)
        fmt.Println("Status Code: ", apiResponse.Response.StatusCode)
    }
}
```



