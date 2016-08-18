import asyncio
import socket
import struct

disco_port = 56712
loop = asyncio.get_event_loop()
magic = b'19589f19'


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


class BeaconListener(object):

    def connection_made(self, transport):
        sock = transport.get_extra_info('socket')
        group = socket.inet_aton('224.0.0.25')
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def datagram_received(self, data, addr):
        print(3, "hi")
        if data.startswith(magic):
            print("Owe, rearwry?", data, addr)


async def beacon():
    t, p = await loop.create_datagram_endpoint(BeaconSender,
                                               allow_broadcast=True,
                                               remote_addr=('255.255.255.255',
                                                            disco_port))


async def start():
    print("a")
    await loop.create_datagram_endpoint(BeaconListener,
                                        local_addr=('0.0.0.0', disco_port))
    print("b")
    await beacon()

try:
    loop.run_until_complete(start())
    loop.run_forever()
except KeyboardInterrupt:
    pass
loop.close()
