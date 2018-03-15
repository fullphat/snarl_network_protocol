# SNP 3.1

1. [Introduction](#introduction)
1. [Overview](#overview)
1. [Message Structure](#message-structure)  
   i. [Requests](#request-structure)  
   ii. [Responses](#response-structure)
1. [Forwarding](#forwarding)
1. [Subscriptions](#subscriptions)
1. [Security](#security)  
   i. [Authentication](#authentication)  
   ii. [Encryption](#encryption)

# Introduction
SNP 3.1 adds a number of improvements to SNP 3.0 while maintaining several of the features the earlier version of the protocol introduced.  Among the changes introduced in SNP 3.1 are:

* **Standardised processing:** every SNP 3.1 request _must_ be accompanied by a resulting SNP 3.1 response.  Furthermore, spurious responses (e.g. forwarded notifications and callbacks) should be sent to a different port that has been created specifically to receive these out-of-cycle messages;

* **Structured messages:** SNP 3.1 defines a number of standard request messages which may be sent by a client;

* **Clearer message format:** SNP 3.1 requests and responses now follow the same template approach;

* **Granular security controls:** servers listening for incoming SNP 3.1 messages should provide the user with the ability to block forwarded notifications, and to require authorisation for such notifications;

* **Flexibility:** callbacks can now be directed to a separate TCP port created specifically for receiving out-of-cycle messages, or POSTed to a URL;

* **More descriptive errors:** in addition to returning the code and name of the error that occurred, SNP 3.1 also defines a further parameter that allows the server to return more context around why the error occurred.

# Overview
## Communication Cycle
A SNP 3.1 conversation is held between a _client_ and a _server_, with the client initiating the request and the server responding to the request appropriately.  The process is as follows:

1. Client opens a connection to the server
1. Client then issues a request
1. Server takes action and issues an appropriate response
1. Client either closes the connection or repeats step 2

The client and server may be on the same physical machine, or they may be on different machines.  If a client wishes to send a request and then close, it _must_ wait until it has received the response from the server, even if it does not plan to do anything with it.

> Callbacks _may_ be received on the port used by the client to issue the requests, however this is not recommended as it requires more complex logic within the client to distinguish between an expected response and an out-of-cycle callback message.  The recommendation is for the client application to create a separate listening socket and pass the port number of that socket when creating notifications.  This then allows the client to run a tight send/receive message loop.

## Other Metrics

### Default Port
SNP 3.1 does not define a standard port.  The end user (or system administrator) is free create SNP 3.1 servers on any valid TCP port.

### Text Encoding
Content values should be encoded as UTF-8.

# Message Structure
A SNP 3.1 request comprises of a _header_, zero or more lines of _content_, and a _terminator_.  Like SNP 3.0, a SNP 3.1 message spans multiple lines and can be a variable number of lines.  The terminator is always `END`.  Each line, including the terminator, must end with a **`CRLF`**.

SNP 3.1 defines two types of message: _Request_ and _Response_.  Both are very similar in format, however requests must include at least one line of content; responses may not include content.  Also, requests must be responded to; responses are not responded to.

## Request Structure

### Header
The header describes the nature of the request:

    {id/version} {action} [{authentication} [{encryption}]]

|Item|Description|
|----|-----------|
|`id/version`|Indicates the version of the protocol to be used.  Always `SNP/3.1`.|
|`action`|Indicates the request type.  There are currently five types of request: `FORWARD`, `NOTIFY`, `REGISTER`, `SUBSCRIBE`, `UNSUBSCRIBE`.|
|`authentication`|The algorithm, key hash and salt used if authentication is required.|
|`encryption`|The encryption algorithm and initialisation value used to secure the message content if it's encrypted.|

### Content
Each line of content is formatted in a similar way to MIME and HTTP headers, as a key/value pair separated with a colon and a space character:

    title: Hello, world!
    text: This is some text...

### Example Request

    SNP/3.1 NOTIFY
    title: Testing...
    text: Hello, world!
    icon: stock:system-info
    END

## Response Structure

### Header
The response header is as follows:

    {id/version} {response_type} [{authentication} [{encryption}]]

|Item|Description|
|----|-----------|
|`id/version`|Returns the highest version of the protocol supported.  Always `SNP/3.1`.|
|`response_type`|Indicates the response type.  There are currently four types of response: `CALLBACK`, `FAILED`, `GOODBYE` and `SUCCESS`.|
|`authentication`|The algorithm, key hash and salt used if authentication is required.|
|`encryption`|The encryption algorithm and initialisation value used to secure the message content if it's encrypted.|

# Forwarding

... Section to be completed ...

# Subscriptions

... Section to be completed ...



# Security

## Authentication
To authenticate a message, the password must be translated into a _key hash_ using a supported _hash algorithm_ and and _salt_.  This is included in the header, as follows:

    SNP/3.1 {action} {hash_algorithm}:{key_hash}.{salt}

See the [Developer Guide](Snarl-Developer-Guide#authentication) for details on supported `hash_algorithm` types and how to generate the `key_hash` and `salt`.

### Example

    SNP/3.1 FORWARD MD5:123456789ABCDEF.CA53559F21004566
    source: SecureBot
    text:Hello, world!
    END

## Encryption
Encrypting a message requires both authentication and a valid encryption algorithm and initialisation value.  The header therefore looks thus:

    SNP/3.1 {action} {hash_algorithm}:{key_hash}.{salt} {encryption_algorithm}:{iv}

The encrypted message still has a header and terminating line, however the content is encrypted into a byte array which is then encoded as a hexadecimal string.

> ![Info](http://fullphat.net/docs/icons/info.png) _Hexadecimal-encoding the message content will double the size of the message packet compared to the same packet unencrypted.  As notifications are by nature intended to be brief, this should not be a significant issue, however if a client typically transfers a large amount of metadata along with the notification, consideration should be given to using a different mechanism to transfer the data - especially if network bandwidth is a concern._


