> ![Warning](http://fullphat.net/docs/icons/warning.png) _This is provisional documentation.  Applications should not attempt to implement any features listed in this document, other than for development or testing purposes.  The documentation is provided for open access to encourage interest in forthcoming features and to solicit feedback and suggestions. It is therefore provided "as is" and is subject to ongoing change and revision._

# Introduction

Oxide is the new name for our SNP/HTTP API.  SNP/HTTP stands for "Snarl Network Protocol over HTTP", which - apart from being a bit of a mouthful - is also starting to become slightly inaccurate, especially with the latest iteration of this API.

> _This guide covers Oxide v2, a completely revised version of SNP/HTTP that follows a RESTful approach and uses a more structured request and response format.  For earlier versions of SNP/HTTP see (here)._

At this time, version 2 is a developing specification.  We welcome contributions and suggestions to the specification but we strongly advise against attempting to implement it in anything other than a test application.

Oxide v2 was first introduced in Snarl 5.0 Beta 2.

![Warning](http://fullphat.net/docs/icons/warning.png) **The response Oxide returns has changed in Snarl 5.0 Beta 6.**  Now, Oxide will return a standard response irrespective of whether the request succeeded or failed.  See Response for more details.

## Benefits

Compared to previous versions of SNP/HTTP, Oxide v2:

* Adopts a RESTful approach
* Will support authorisation
* Defines a small number of endpoints
* Uses JSON as the mechanism of choice for passing data back and forth
* Provides a greater level of access to Snarl metadata than other transports (including Win32)

## Standards

Oxide enforces a number of standards in order to ensure a consistent approach.  If you've worked with other RESTful APIs, these should be no different:

* `POST` methods create or add artefacts
* `GET` methods retrieve information
* `DELETE` methods delete or remove artefacts
* All `POST` methods must use `application/json` as the content type
* The custom header `oxide-authorisation` will be used to authorise communication with Snarl

# Getting Started
Most applications will use an existing wrapper library in the language of your choice, but it's important to familiarise yourself with the underlying API HTTP methods first.

There's no easier way to get started than by using Curl, so let's dive straight in and say hello to Snarl:

**`curl "http://localhost:8080/v2/"`**

Snarl responds with:

`Welcome to the Oxide version 2 API!  Note that this API is in development and, as such, should only be used for testing purposes.  Find out more about Oxide here: https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Developer-Guide`

The first thing to note is that we're using Curl to talk to Snarl.  Curl comes installed on OS X and most mainstream Linux distributions.  If you're running Windows, you can [download it from here](https://curl.haxx.se/download.html).  We use Curl in this guide as it's an excellent way to show the raw request and response content.

We're talking to Snarl running on `localhost` and on port 8080, but we could just as well be talking to it on another server on our network, or even over the Internet.  See (here) for how to configure Oxide to listen on a particular port and (here) for how to get Windows to listen on more than just `localhost`.

Now we've proven that Snarl's listening, let's display a notification:

**`curl -H "Content-Type: application/json" "http://localhost:8080/v2/notifications" -d '{ "title": "Hello, world!" }'`**

    {
      "meta": {
        "code": 201,
        "text": "Created"
      },
      "data": {
        "id": "a7fdb4de-e462-4866-89ce-7b4d28929255"
      }
    }

There's a bit going on here, so let's step through it...

Firstly, we're talking to the [`notifications`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-API-Reference#notifications-1) Oxide endpoint and, because we want to create a notification, we need to `POST` the data to Snarl (this is implied using the `-d` Curl switch) and we need to set the `Content-Type:` header to `application/json`.  Finally, we pass the following nugget of JSON in the request body to describe the notification we want:

    {
      'title': 'Hello, world!'
    }

Snarl responds with:

    {
      "meta": {
        "code": 201,
        "text": "Created"
      },
      "data": {
        "id": "a7fdb4de-e462-4866-89ce-7b4d28929255"
      }
    }

And the following appears on screen:

![Motz Bazix](http://fullphat.net/docs/snphttp/hello_world_basic.png)

This generates probably one of the most simplest notifications you can create, but it shows just how easy it is to talk to Snarl.  Let's really crank things up a notch and change the icon:

**`curl -H "Content-Type: application/json" "http://localhost:8080/v2/notifications" -d '{ "title": "Hello, world!", "icon": "!misc-hammer" }'`**

Gives us this back from Snarl:

    {
      "meta": {
        "code": 201,
        "text": "Created"
      },
      "data": {
        "id": "2d381ea2-7002-48f5-8d0f-d25543b97a2d"
      }
    }

And this on screen:

![L33t iconz](http://fullphat.net/docs/snphttp/hello_world_with_icon.png)

Note that Snarl returns a different `id` this time.  This is the notification's unique identifier and, as we just created a new notification, we've got a new identifier.


# Authorisation

**Not currently implemented.**  However, the hash algorithm, key hash and salt would be passed in the `oxide-authorisation` header of each request if the transport is password-protected.  This would use the same format as SNP 3.1.

### Example

`oxide-authorisation: MD5:0000000000000000.123456`

# Registering an application

Applications are registered by `POST`ing an Oxide [`registration`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#registration) object to Snarl.  Let's say we want to register application `foo.bar` with Snarl:

**`curl -H "Content-Type: application/json" "http://192.168.1.1:8080/v2/apps" -d "{ \"app-id\": \"foo.bar\", \"title\": \"Foo.Bar\" }"`**

Returns:

    {
      "meta": {
        "code": 201,
        "text": "Created"
      },
    "data": {
        "app-id": "foo.bar",
        "title": "Foo.Bar",
        "type": "Application",
        "first_registered": "Sun, 11 Mar 2018 19:05:21 GMT",
        "last_registered": "Sun, 11 Mar 2018 19:05:21 GMT",
        "is_authorised": true,
        "is_secured": false,
        "icon": "C:\\Users\\foo\\AppData\\Local\\Temp\\b5753472-8fb7-42c4-949d-df80ef025bfd.png"
      }
    }

Indicating that the application was successfully registered.  Note that the `data` object in the response contains the corresponding [`application`](https://github.com/fullphat/snarl_network_protocol/wiki/Oxide-Objects#application) object for the registered application.

Snarl R5.0 only needs an application to be registered once rather than each time Snarl is launched.


# Creating an event


# Displaying a notification

We saw above how to create a simple notification using the built-in Grampf application to handle it.  Normally however, you'll register an application, create events, and then generate notifications against that application and one of the events you've added.

This is done by `POST`ing to the `/v2/notifications/` endpoint, passing the application identifier and event identifier to use in the URI, and details about the notification itself in the request body.

## Examples

Let's say we have an application registered as `app` with an event called `foo`.  We can create a simple notification as follows:

**`curl -H "Content-Type: application/json" "http://localhost:8080/v2/notifications/app/foo" -d '{ "title": "Hello, world!" }'`**

    {
      "success": {
        "id": "dc506c1b-bab8-4bdc-b8bb-ebf91a53366c"
      }

And the same notification, but using an icon that's stored on the machine displaying the notification:

**`curl -H "Content-Type: application/json" "http://server:8080/v2/notifications/app/foo" -d '{ "title": "Hello, world!", "icon": "c:/icons/home.png" }'`**


# Advanced Techniques

## Listening on more than just `localhost`

By default, Windows 7 and above limits the ability for web servers to only be able to listen for incoming connections on `localhost`.  To remove this restriction, do the following on the machine running Snarl:

* Launch an administrative Command Prompt
* Enter the following, replacing `8080` with the port number you've configured Snarl to listen for Oxide requests on:

`netsh http add urlacl url=http://+:8080/ user=Everyone listen=yes`

* Restart the listener by disabling it and then re-enabling it within Snarl.
