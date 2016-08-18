aiodiscovery
===========
Service discovery using asyncio.


About
--------
A library for doing service discovery.  Uses a combination of multicast and
broadcast datagram packets to find other services of the same make.  Use this
library for services running in a cluster to discover the IP/Ports of those
services.


Requirements
--------
* Network supporting broadcast and multicast packets.  The TTL for the multicast
  packets can be changed but defaults to 3.


Compatibility
--------

* Python 3.5+
