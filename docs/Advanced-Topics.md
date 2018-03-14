
# Subscription Servers

## What is a Subscription Server?
A subscription server is a component that handles both the `SUBSCRIBE` and `UNSUBSCRIBE` SNP/3.1 requests such that it can then act as a source of notifications to a remote instance of Snarl.

## Why implement a subscription server?
Although applications can forward unsolicited notifications to Snarl, this feature could be abused and, in extreme circumstances, could be used as a Denial of Service attack on a user, or group of users.  For this reason, system administrators may decide to disable handling of unsolicited notifications.

Subscriptions provide a wrapper around forwarded notifications in that a user can _subscribe_ to notifications from a server.  Notifications sent from the server are then aligned with the subscription, providing an extra level of assurance.

## Accepting Subscriptions
The server should support both `reply-port` subscriptions and `forward-to` subscriptions, however it may choose to only support one of these types.  It should respond to requests it doesn't support with a `?not_implemented?` error.

Servers should also reject requests which supply _both_ `reply-port` and `forward-to` values as this is considered ambiguous and therefore an error.  The server should respond with a `?invalid_args?` error in this instance.

## Managing Subscribers
Subscribers should be tracked when they appear and disappear, especially in terms of detecting (and rejecting) duplicate subscriptions or unsubscriptions.  The `uid` value supplied in both the `SUBSCRIBE` and `UNSUBSCRIBE` request, along with the IP address of the client making the request, can be used to identify a subscriber.

Duplicate subscriptions should be responded to with a `?duplicate_subscription?` error; duplicate (or spurious) unsubscriptions should be responded to with a `?not_found?` error.

Subscriptions with a `uid` parameter should be responded to with a `?arg_missing?` error.

## Housekeeping
A server may need to stop serving notifications (for example, it may need to restart after updating).  In this instance it _must_ notify all existing subscribers that it is stopping by issuing a `GOODBYE` response to each connected subscriber.  The `GOODBYE` response must be sent to the `reply-port` or `forward-to` URL and should include the `uid` included in the individual subscription.

On receiving a `GOODBYE`, the client should perform its own housekeeping, but is entitled to re-try the subscription after a short period of time (no less than 30 seconds).  For this reason, the server should only ensure it processes SNP requests when it is ready to handle them, or it can return a suitable error response (for example `?server_busy?`) until it is ready to do so.



