> ![Warning](http://fullphat.net/docs/icons/warning.png) _This is provisional documentation.  Applications should not attempt to implement any features listed in this document, other than for development or testing purposes.  The documentation is provided for open access to encourage interest in forthcoming features and to solicit feedback and suggestions. It is therefore provided "as is" and is subject to ongoing change and revision._

1. [Overview](#overview)
1. [Objects](#objects)
1. [Endpoints](#endpoints)

# Overview

### Base URI
The base URI for SNP/HTTP V2 is `/v2`.  So, if Snarl is running on host `ninja`, and it's listening for SNP/HTTP on port 4444, an example call would be:

`http://ninja:4444/v2/authorise`

### Content
`POST` requests require a request body that is formatted as JSON.  All responses (except when calling the root endpoint) are formatted as JSON.

### Arguments
With the exception of `/authorise`, every request must include an `access_token` as an argument within the URL query.  For example:

`GET` `http://ninja:4444/v2/notifications?access_token=00000001`

### Headers
All `POST` requests must set `Content-Type` to `application/json`.  Other than that, no specific headers are required.

### Methods

* `GET` requests are used to return information

* `POST` requests create new things like application registrations, events and notifications

* `DELETE` requests unregister applications, remove events and hide notifications

### Responses
Every request generates the same response.  The response will contain two objects:

* [`meta`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#meta) - which indicates whether the request was successful or not.  If the request was not successful, the meta object may contain an explanation of why it failed

* [`data`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#data) - contains information relevant to the request.  If the request was not successful, an empty data object will be returned

#### Example Success Response

    {
      "meta": {
        "code": 201,
        "text": "Created"
      },
      "data": {
        "id": "a7fdb4de-e462-4866-89ce-7b4d28929255"
      }

#### Example Failure Response

    {
      "meta": {
        "code": 404,
        "text": "NotFound",
        "reason": "Application 'foo.bar' isn't registered."
      },
      "data": {}
    }

# Objects

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


# Endpoints
The following endpoints are currently defined:

| Endpoint|Description|
| ------------- |-------------|
| [`/apps`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Endpoints#apps)|Manages application registrations|
| [`/events`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Endpoints#events)| Manages application event creations and deletions|
| [`/notifications`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Endpoints#notifications)|Manages notifications|
| [`/info`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Endpoints#info)|Returns information about the running instance of Snarl|

