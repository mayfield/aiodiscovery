"""
Service discovery using asyncio.
"""

import asyncio
import socket
import struct


class BeaconSender(object):

    def connection_made(self, transport):
        print("hi", transport)
        transport.sendto(magic)

    def datagram_received(self, data, addr):
        print(1, "hi")
        message = data.decode()
        if message.startswith(magic):
            print("Owe, rearwry?", data, addr)

    def error_received(self, exc):
        raise exc


class MCBeaconListener(object):

    def __init__(self, addr, magic, service_tag=None):
        self.addr = addr
        self.magic = magic
        self.service_tag = service_tag

    def connection_made(self, transport):
        print('conn made')
        sock = transport.get_extra_info('socket')
        group = socket.inet_aton(self.addr)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def datagram_received(self, data, addr):
        print('datagram_recv', data, addr)
        if not data.startswith(self.magic):
            return


class BCBeaconListener(object):

    def __init__(self, addr, magic, service_tag=None):
        self.addr = addr
        self.magic = magic
        self.service_tag = service_tag

    def connection_made(self, transport):
        print('conn made')
        sock = transport.get_extra_info('socket')
        group = socket.inet_aton(self.addr)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def datagram_received(self, data, addr):
        print('datagram_recv', data, addr)
        if not data.startswith(self.magic):
            return


async def beacon():
    t, p = await loop.create_datagram_endpoint(BeaconSender,
                                               allow_broadcast=True,
                                               remote_addr=('255.255.255.255',
                                                            disco_port))


class MCDiscoverer(object):
    """ Similar to a asyncio.Server object in interface. """

    def __init__(self, host='225.11.8.84', port=35311, magic=b'19589f19',
                 loop=None):
        self.addr = host, port
        self.beacon_task = None
        self.magic = magic
        self.join_awaitables = []
        self.leave_awaitables = []
        self.tranport = None
        self.running = False
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop

    def on_join(self, awaitable, service_tag=None):
        """ Run the awaitable when a new node is detected. """
        self.join_awaitables.append(awaitable)

    def on_leave(self, awaitable, service_tag=None):
        """ Run the awaitable when a new node is detected. """
        self.join_awaitables.append(awaitable)

    async def run(self):
        factory = lambda: MCBeaconListener(self.addr, self.magic)
        endpoint = self.loop.create_datagram_endpoint
        self.transport = await endpoint(factory, local_addr=self.addr)[0]
        self.beacon_task = self.loop.create_task(self.repeat_beacon())
        self.running = True

    async def repeat_beacon(self):
        while self.closing:

    def close(self):
        assert self.running
        self.running = False
        if self.beacon_task is not None:
            self.beacon_task.cancel()
        self.transport.cancel()

    async def wait_closed(self):
        pass


# XXX TEST
try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_mcast_discovery(
    loop.run_until_complete(start())
    loop.run_forever()
except KeyboardInterrupt:
    pass
loop.close()
