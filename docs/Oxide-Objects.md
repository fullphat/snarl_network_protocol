## Contents

|Object|Description|
|------|-----------|
|[`application`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#application)|Describes a particular application registration|
|[`applications`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#applications)|Contains an array of [`application`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#application) objects
|[`data`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#data)|Response data object|
|[`event`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#event)|Describes a single event class|
|[`events`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#events)|Contains an array of [`event`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#event) objects
|[`meta`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#meta)|Response metadata|
|[`notification`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#notification)|Describes a particular notification|
|[`notifications`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#notifications)|Contains a list of [`notification`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#notification) objects
|[`registration`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#registration)|Provides information about an application to be registered|

***


## `application`
Returned by either `GET` `/apps/:appId` or `GET` `/apps/` (as part of the returned [`applications`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#applications) object):

|Parameter|Type|Description|
|---------|----|-----------|
|`app-id`|String|The application identifier|
|`first_registered`|String|Date and time when the application was first registered with Snarl, in RFC1123 format|
|`icon`|String|Path to the application's icon|
|`is_authorised`|Bool|Whether or not the application is authorised to display notifications|
|`is_secured`|Bool|Whether or not the application is password-protected|
|`title`|String|The name of the application as displayed to the end user|
|`type`|String|The registration type, which can be either `application` or `extension`|

### Example

`curl "http://192.168.1.1:8080/v2/apps/foo.bar"`

    {
      "meta": {
        "code": 200,
        "text": "OK"
      },
      "data": {
        "app-id": "foo.bar",
        "title": "Foo.Bar",
        "type": "Application",
        "first_registered": "Thu, 08 Mar 2018 17:49:53 GMT",
        "is_authorised": true,
        "is_secured": true,
        "icon": "C:\\foo.png"
      }
    }

***

## `applications`
An array of [`application`](#application) objects.  This is returned by `GET` `/apps`.

### Example

`curl "http://192.168.1.1:8080/v2/apps/"`

    {
      "meta": {
        "code": 200,
        "text": "OK"
      },
      "data": [
        {
          "app-id": "foo.bar",
          "title": "Foo.Bar",
          "type": "Application",
          "first_registered": "Sat, 20 May 2017 22:16:45 GMT",
          "last_registered": "Sun, 11 Mar 2018 14:26:11 GMT",
          "is_authorised": true,
          "is_secured": true,
          "icon": "C:\\foo.png"
        },
        ...
      ]
    }

***

## `data`
Returned as part of the standard response message.  This object will contain content relevant to the function that was called.  Note that the object will _always_ be present, but may be empty.

### Example

With `id` integer 528:

    {
      "data": {
        "id": 528
      }
    }

Nothing to return:

    {
      "data": {}
    }

***

## `event`
An `event` object describes a single event class.  These are typically used when calling `POST` `/events` to add one or more events to an application registration.

|Parameter|Type|Description|
|---------|----|-----------|
|`action`|String|The "When..." action description to display when this event class is used in a rule|
|`app-id`|String|The application identifier this event class relates to|
|`defaults`|Object|A `defaults` object containing notification defaults to use when applicable|
|`event-id`|String|The internal identifier of the event class|
|`name`|String|The name of the event class as presented to the end user|

***

## `events`
An `events` object describes one or more event classes.  This object is passed to `POST` `/events` when adding events to an application registration.

|Parameter|Type|Description|
|---------|----|-----------|
|`events`|Array|Array of [`event`](#event) Objects|

***

## `meta`
Returned as part of the standard Oxide response message:

|Item|Type|Description|
|----|----|-----------|
|`code`|Int|the HTTP status code as an integer|
|`text`|String|the HTTP status code as human-readable text|
|`reason`|String|further explanation of what went wrong|

Note that `reason` may not be present if there is no further explanation available.

### Example

    {
      "meta": {
        "code": 404,
        "text": "NotFound",
        "reason": "Application '\"foo\"' isn't registered."
      }
    }

***

## `notification`
A `notification` object describes an individual notification.

### Parameters

|Name|Type|Description|
|----|----|-----------|
|`app_id`|String|The unique identifier of the application that generated the notification|
|`created`|String|Date and time when the notification was created in RFC1123 format|
|`data-*`|String|Any `data-` values that were supplied when the notification was created|
|`duration`|Integer|Number of seconds the notification was displayed for (or will be displayed for)|
|`event_id`|String|The event class used to display the notification, can be `""` if no event class was specified|
|`icon`|String|The path to the icon used, if one was specified|
|`id`|String|The notification's unique identifier|
|`is_visible`|Boolean|True if the notification is still visible on screen, False otherwise|
|`last_seen`|String|Date and time the notification was last displayed in RFC1123 format - this can be `""` if the notification hasn't been displayed yet|
|`priority`|Integer|A number between -63 and +63 where -63 is the lowest priority and 63 the highest - currently only priorities between -2 to +2 inclusive should be used, other values are reserved for future use|
|`scheduled`|String|Date and time the notification is/was scheduled for display in RFC1123 format|
|`text`|String|The notification text|
|`title`|String|The notification title|

### Example

    "notification": {
      "id": "b31a5434-1ee5-4864-9e0c-749781f5c435",
      "is_visible": false,
      "created": "Thu, 30 Mar 2017 19:40:58 GMT",
      "scheduled": "Thu, 30 Mar 2017 19:40:58 GMT",
      "last_seen": "Thu, 30 Mar 2017 19:40:58 GMT",
      "app_id": "c77cf0c7-3a18-4e11-81e7-969a957589d4",
      "event_id": "",
      "title": "Hello, world!",
      "text": "",
      "icon": "grampf.png",
      "duration": 10,
      "priority": 0
    }

***

## `notifications`
A `notifications` object contains an array of `notification` objects.

### Example

    "notifications": [
      {
        "id": "b31a5434-1ee5-4864-9e0c-749781f5c435",
        "is_visible": false,
        "created": "Thu, 30 Mar 2017 19:40:58 GMT",
        "scheduled": "Thu, 30 Mar 2017 19:40:58 GMT",
        "last_seen": "Thu, 30 Mar 2017 19:40:58 GMT",
        "app_id": "c77cf0c7-3a18-4e11-81e7-969a957589d4",
        "event_id": "",
        "title": "Hello, world!",
        "text": "",
        "icon": "grampf.png",
        "duration": 10,
        "priority": 0
      },
      {
        "id": "83f9d359-9f1a-4a78-b32d-73e3b0cf3e65",
        "is_visible": true,
        "created": "Thu, 30 Mar 2017 19:41:00 GMT",
        "scheduled": "Thu, 30 Mar 2017 19:41:00 GMT",
        "last_seen": "Thu, 30 Mar 2017 19:41:00 GMT",
        "app_id": "c77cf0c7-3a18-4e11-81e7-969a957589d4",
        "event_id": "",
        "title": "Hello, world!",
        "text": "",
        "icon": "rampf.png",
        "duration": 10,
        "priority": 0
      },
      {
        "id": "017412cd-989d-4540-ba4b-29f0108db54c",
        "is_visible": true,
        "created": "Thu, 30 Mar 2017 19:41:01 GMT",
        "scheduled": "Thu, 30 Mar 2017 19:41:01 GMT",
        "last_seen": "Thu, 30 Mar 2017 19:41:01 GMT",
        "app_id": "c77cf0c7-3a18-4e11-81e7-969a957589d4",
        "event_id": "",
        "title": "Hello, world!",
        "text": "",
        "icon": "grampf.png",
        "duration": 10,
        "priority": 0
      }
    ]

***

## `registration`
Used when calling `POST` `/apps` to register an application:

|Parameter|Type|Description|
|---------|----|-----------|
|`app-id`|String|Required.  The application identifier|
|`title`|String|Required.  The name of the application as displayed to the end user|
|`icon`|String|Recommended.  The icon to use, which can be any (standard icon type)|

### Example

`curl -H "Content-Type: application/json" "http://192.168.1.1:8080/v2/apps" -d "{ \"app-id\": \"foo.bar\", \"title\": \"Foo.Bar\" }"`


