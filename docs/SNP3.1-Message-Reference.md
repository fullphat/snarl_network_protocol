1. [Introduction](#introduction)
1. [Requests](#requests)  
   i. [`FORWARD`](#forward)  
   ii. [`NOTIFY`](#notify)  
   iii. [`REGISTER`](#register)  
   iv. [`SUBSCRIBE`](#subscribe)  
   v. [`UNSUBSCRIBE`](#unsubscribe)
1. [Responses](#responses)  
   i. [`FAILED`](#failed)  
   ii. [`SUCCESS`](#success)
1. [Out-of-Cycle Messages](#out-of-cycle-messages)  
   i. [`CALLBACK`](#callback)  
   ii. [`GOODBYE`](#goodbye)  


# Requests

## `FORWARD`

### Required Entries

|Name|Description|
|----|-----------|
|`source`|The name of the application sending the forwarded notification|

### Optional Entries


### Notes

* Must not include `app-id:` or `event-id` parameters;
* The server will use the client's IP address to help identify the source of the forwarded message.

### Example

    SNP/3.1 FORWARD
    source: My App
    title: Daily Notice
    text: The fire alarm will be tested at 11am today
    icon: stock:system-info
    END


## `SUBSCRIBE`

### Required Entries

|Name|Description|
|----|-----------|
|`forward-to`|The URL to send subsequent forwarded notifications to.|
|`reply-port`|The port to send subsequent forwarded notifications to.|
|`uid`|A unique identifier for the subscription.|

### Optional Entries

|Name|Description|
|----|-----------|
|`filter`|One or more application identifiers separated by semicolons.|
|`filter-type`|Either `inclusive` or `exclusive`.|

### Notes

* The client can request all notifications, or only certain notifications, however the server ultimately decides which notifications it will forward;
* The server may require authentication - if so, the authentication details must be included in the request header in the normal way.  See the [Security](security) section for further information;
* Subscription servers _should_ handle both types of forwarding, however they are not obligated to do so.  When sending a `SUBSCRIBE` request, the client _must_ check the returned status to ensure the server accepted the request;
* The uid should be a string of alphanumeric characters (a [GUID](https://msdn.microsoft.com/en-us/library/system.guid(v=vs.110).aspx) is a good example);
* Supplying both `reply-port` and `forward-to` is invalid and will return an error;
* See [this guide](Subscribing-to-notifications) for more detail - and a worked example - on subscriptions.


A subscription is a request from a client to a server where the client asks to receive notifications from the server.  The notifications will be sent as forwarded messages, rather than traditional notifications.  

Subscriptions can take two forms: notifications can be forwarded to a URL as an HTTP `POST` request, or they can be sent as an SNP 3.1 `FORWARD` message to a port on the same computer as the client.

Subscriptions must include a unique identifier (uid) which is used when unsubscribing and should also be sent by the server when it needs to issue a `GOODBYE` response.  


### Examples

Straightforward request which asks for notifications to be sent to port 5000:

    SNP/3.1 SUBSCRIBE
    uid: my_lame_uid
    reply-port: 5000
    END

Same, but using authentication:

    SNP/3.1 SUBSCRIBE MD5:ABCDEF1234.9876543210
    uid: my_lame_uid
    reply-port: 5000
    END

Request which asks for notifications to be sent to `http://mysever:4444/bucket/`:

    SNP/3.1 SUBSCRIBE
    uid: my_lame_uid
    forward-to: http://mysever:4444/bucket/
    END

## `UNSUBSCRIBE`

### Required Entries

|Name|Description|
|----|-----------|
|uid|The unique identifier used in the initial subscription.|

### Optional Entries
None.

### Notes

* The request must be issued from the same IP address that was used for the initial subscription.  
* Once a client is unsubscribed, it may resubscribe using either the same or a different password.

### Example

    SNP/3.1 UNSUBSCRIBE
    uid: my_lame_uid
    END



# Responses

## `FAILED`
A `FAILED` response indicates the request could not be processed by the server for some reason.

### Standard Content

|Name|Requirement|Description|
|----|-----------|-----------|
|`error-number`|Mandatory|The Snarl status code of the error as a positive integer|
|`error-name`|Mandatory|The Snarl status code as a string|
|`reason`|Mandatory|Further context or supporting information explaining the error.  Must be included, but may be blank|

### Optional Content
Servers may include additional information in the form of `x-` header entries.  Servers _must not_ return `data-` entries however. 

### Notes
None.

### Example

    SNP/3.1 FAILED
    error-number: 202
    error-name: NotRegistered
    reason:
    END




## `SUCCESS`

### Standard Content
None.

### Optional Content
A success response may contain additional information, however this will be relevant to the request the response pertains to.

Servers may include additional information in the form of `x-` header entries.  Servers should not return `data-` entries however.

### Notes

### Examples

Example returning some data:

    SNP/3.1 SUCCESS
    data-example: some data here
    data-value: 23
    END

Example returning no extra data:

    SNP/3.1 SUCCESS
    END


# Out-of-Cycle Messages

## `CALLBACK`
A callback message is sent either to a listening TCP port on the client machine that created the notification, or to a URL as an HTTP `POST` request.

Due to the asynchronous nature that notifications may appear, and when a user may react to a notification (if at all), callback messages can arrive at any time and in any sequence.  The receiving client can determine which callback message refers to which notification using the `uid` parameter, any `data-` values included in the notification, or a combination of the two.

### Standard Content
None.

### Optional Content

|Name|Value|
|----|-----|
|`uid`|The uid supplied when the notification was created (if one was provided)|
|`data-*`|Any data parameters supplied when the notification was created|

### Notes

* The server may also include additional metadata in terms of `x-` headers.

### Example
The following callback message indicates that a notification was closed by the end user.  The notification was created with a `uid` of `my_lame_uid` and included some additional `data-` parameters:

    SNP/3.1 CALLBACK
    uid: my_lame_uid
    data-guardian: Len
    data-wossname: cheese
    data-place: On The Bus
    END

## `GOODBYE`
A `GOODBYE` message is sent by a subscription server when it is closing.  This can be used to notify subscribers that they should no longer expect to received forwarded notifications from the server.  The subscriber is free to attempt to reconnect (as the server may simply be restarting), but should wait a short period of time (at least 30 seconds) before doing so.

### Standard Content

|Name|Value|
|----|-----|
|`uid`|The UID specified by the subscriber when it originally subscribed.|

### Optional Content

|Name|Value|
|----|-----|
|`x-reason`|Human readable text indicating why the server is stopping|
|`x-retry-after`|Number of seconds clients should wait before retrying a connection to the server|

### Notes
None.

### Example

    SNP/3.1 GOODBYE
    uid: some_uid
    END



