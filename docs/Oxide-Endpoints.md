## Contents

| Endpoint|Description|
| ------------- |-------------|
| [`/apps`](#apps)|Manages application registrations|
| [`/authorise`](#authorise)|Generates an `access_token` that allows access to the rest of the API|
| [`/events`](#events)| Manages application event creations and deletions|
| [`/notifications`](#notifications)|Manages notifications|
| [`/info`](#info)|Returns information about the running instance of Snarl|


## `/apps`
This endpoint manages application registrations.  Your application can register multiple applications with Snarl, however typically it would only ever register one.

|Method|Function|Description|
|------|--------|-----------|
|`POST`|[`/apps`](#post-apps)|Registers an application|
|`DELETE`|[`/apps/:appId`](#delete-apps)|Unregisters an application|
|`GET`|[`/apps/:appId`](#notifications)|Returns an [`application`](#application) which contains information about the specified application|


### `POST` `/apps`
Registers an application with Snarl.

#### Path Arguments

None

#### Data Arguments

|Name|Status|Description|
|----|------|-----------|
|`app-id`|Required|The (application identifier) to use.|
|`title`|Required|The application’s name as displayed to the end user.|
|`hint`|Optional|Free-form hint text that describes the application to the end user.|
|`icon`|Optional|The icon to use, this can be any of the standard (Snarl API icon types).|

#### Response
If the application was registered successfully, you’ll get a [`success`](#success) response with the application’s identifier included.  If the application wasn’t registered successfully, you’ll get a [`failed`](#failed) response with suitable error information.

Possible reasons for failure include:
* An application with the same identifier is already registered with a different `access_token`
* Either of the `title` or `app-id` parameters were missing or invalid
* No access token was provided

#### Example

`curl http://ninja:4444/v2/apps?access_token=00000001 -d "{ 'app-id': 'myapp',  'title': 'My App' }"`

    {
      "success": {
        "app-id": "myapp"
      }
    }


### `DELETE` `/apps/{app-id}`
Unregisters an application.

#### Required Arguments

|Name|Description|
|----|-----------|
|`app-id`|The application identifier for the registration to delete.|

#### Optional Arguments
None.

#### Response
If the application was unregistered successfully, you’ll get a [`success`](#success) response with the application’s identifier included.  If the application wasn’t unregistered successfully, you’ll get a [`failed`](#failed) response with suitable error information.

Possible reasons for failure include:
* The application isn't registered
* The application was registered with a different `access_token`
* The `app-id` parameter was missing or invalid
* No access token was provided

#### Example

`curl -X DELETE http://ninja:4444/v2/apps/myapp?access_token=00000001`

    {
      "success": {
        "app-id": "my app"
      }
    }


### `GET` `/apps`
Retrieves a list of all applications registered using the provided `access_token`.

#### Arguments
None.

#### Response
If successful, you'll get a `Success` object that contains an `Applications` object which lists all the registrations you've made.  If you've not made any registrations, you'll still get the `Applications` object, only it will be empty.

If the request fails, you’ll get a (`failed`) response with suitable error information.  Possible reasons for failure include:

* No access token was provided
* An invalid access token was provided





### `GET` `/apps/{app-id}`
Returns information about a previously registered application

#### Example
`curl http://ninja:4444/v2/apps/myapp?access_token=00000001`

#### Response
If the application is registered, you’ll get a [`success`](#success) response that contains an [`application`](#application) object which describes the application.  If the application wasn’t registered successfully, you’ll get a (`failed`) response with suitable error information.  Possible reasons for failure include:
* The application isn't registered
* No access token was provided
* The application was registered using a different access token, or a different transport

***

## `/authorise`
This endpoint manages authenticating clients.  At this time it only exposes a single function, the endpoint itself.

### `GET` `/authorise`
Generates an `access_token` so the calling application can access the rest of the API.

#### Response
If authentication was successful, you’ll get a [`success` object](#success) returned with the `access_token` included.

#### Example

    {
      "success": {
        "access_token": "3fd94a8e-3add-48ec-ac29-649c9a2576a4"
      }
    }

***

## `/events`
Manages notification event classes.  The following functions are defined:

|Method|Function|Description|
|------|--------|-----------|
|`POST`|[`/events/:appId`](#post-events)|Adds one or more events to an application|
|`DELETE`|[`/events/:appId/:eventId`](#delete-events)|Removes a specific event class from an application|
|`DELETE`|[`/events/:appId`](#delete-events)|Removes all events from the specified application|
|`GET`|[`/events/:appId`](#get-events)|Returns an [`events`](#events) object which contains details of the event classes assigned to the specified application|


### `POST` `/events/:appId`
Adds one or more events to the application specified by `:appId`.  If a particular event exists, it will be updated with any new information provided.

#### Path Arguments

|Name|Status|Description|
|----|------|-----------|
|`:appId`|Required|Application identifier.|

#### Data Arguments

|Name|Status|Description|
|----|------|-----------|
|`events`|Required|A completed [`events`](#events) object containing the event classes to add or update.|

#### Response

Returns `200` if all events were added or updated successfully, or one of the following errors:

|Status Code|Likely cause|
|-----------|-----------|
|`400`|Incorrectly formatted data or at least one `event` object missing an `event-id` parameter|
|`401`|Transport authentication or application password protection mismatch|
|`404`|Application `:appId` not registered|

Note that any classes that were added will remain, but processing of further events will stop.

#### Example

**`curl -H "Content-Type: application/json" "http://192.168.1.110:8080/v2/events/app" -d '{ "events": [ { "event-id": "foo", "name": "Event Foo" } ] }'`**

    {
      "success": {}
    }


### `GET` `/events/:appId`
Returns the events associated with the application specified by `:appId`.

#### Required Arguments

|Name|Description|
|----|-----------|
|`app-id`|The application identifier to retrieve information on.|

#### Optional Arguments
None.

#### Response
If the information was retrieved a [`success`](#success) object with an [`application`](#application) object included.  If an error occurs, a [`failed`](#failed) object will be returned.

Possible reasons for failure include:
* The specified application wasn't registered using the provided `access_token`.

#### Example

`x`

    {
      "success": {
        "app-id": "my app"
      }
    }


### `DELETE` `/events/{app-id}/{event-id}`
Removes the event with `{event-id}` from registration `{app-id}`.

#### Required Arguments

|Name|Description|
|----|-----------|
|`app-id`|The application identifier to retrieve information on.|
|`event-id`|The event identifier to retrieve information on.|

#### Optional Arguments
None.

#### Response
N.

Possible reasons for failure include:
* N

#### Example

`x`

    {
      "success": {
        "app-id": "my app"
      }
    }


***


## `/notifications`
This endpoint manages notifications.

            // POST    /v2/notifications/:appId[/:eventId]
            // GET     /v2/notifications/:appId[/:eventId]
            // GET     /v2/notifications/:guid
            // DELETE  /v2/notifications/:guid


|Method|Function|Description|
|------|--------|-----------|
|`POST`|[`/notifications/[:appId[/:eventId]]`](#x)|Displays a notification|

### `POST` `/notifications/[:appId[/:eventId]]`
Creates a new notification.

#### Path Arguments

|Name|Status|Description|
|----|------|-----------|
|`:appId`|Optional|Application identifier.|
|`:eventId`|Optional|Event identifier.|

#### Data Arguments

|Name|Status|Description|
|----|------|-----------|
|`callback-dismissed`|Optional|A (managed callback) to process if the user dismisses the notification|
|`callback-expired`|Optional|A (managed callback) to process if the notification expires without any user interaction|
|`callback-invoked`|Optional|A (managed callback) to process if the user invokes the notification|
|`duration`|Optional|The number of seconds the notification should be displayed on-screen for|
|`icon`|Optional*|The notification icon - this can be any (standard Snarl icon)|
|`password`|Optional|Password used during application registration, if one was provided|
|`priority`|Optional|The notification priority - can be one of `urgent`, `high`, `normal`, `low` or `ad hoc`|
|`scheduled`|Optional|The date and time when this notification should be displayed|
|`sound`|Optional|The sound to play|
|`text`|Optional*|The notification body text|
|`title`|Optional*|The notification title|

#### Notes
* One of `title`, `text` or `icon` must be provided.
* If the application was registered using a password, the same password must be included.  Use of passwords is highly recommended, see the (security) section for more information.
* Using the default event is not recommended - see the (developer guidelines) for more details|


#### Example
    {
        "title":"Hello, world!",
        "text":"Just a test...",
        "icon":"!misc-chair",
        "data-misc":"hello word",
        "data-number":"42",
        "callback-invoked":"http-post:http://localhost:8080/callback"
    }

### `GET` `/notifications/{guid}`
Returns information about a previously created notification

#### Required Arguments

|Name|Description|
|----|-----------|
|`a`|A.|

#### Optional Arguments
None.

#### Response
N.

Possible reasons for failure include:
* N

#### Example

`x`

    {
      "success": {
        "app-id": "my app"
      }
    }


### `DELETE` `/notifications/{guid}`
Removes a notification from the screen

#### Required Arguments

|Name|Description|
|----|-----------|
|`a`|A.|

#### Optional Arguments
None.

#### Response
N.

Possible reasons for failure include:
* N

#### Example

`x`

    {
      "success": {
        "app-id": "my app"
      }
    }

***

## `/info`
This endpoint provides information about Snarl itself.

### `GET` `/info/version`
Returns Snarl version information.

#### Required Arguments
None.

#### Optional Arguments
None.

#### Response
So long as Snarl is running, the following will be returned:

|Name|Type|Description|
|----|----|-----------|
|`api_version`|Integer|The (API version) of Snarl|
|`beta_release`|String|Details of the beta release of Snarl, or `""` if a general release version is running|
|`release_number`|String|The release of Snarl as a string|
|`snp_http_version`|String|The maximum version of SNP/HTTP supported by the running instance of Snarl|

#### Example
`curl http://host:4444/v2/info/version?access_token=00000001`

    {
      "success": {
        "release_number": "5.0",
        "beta_release": "Beta 2",
        "api_version": 47,
        "snp_http_version": "2.1"
      }
    }


