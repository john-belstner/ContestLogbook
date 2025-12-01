import socket
import struct
import threading
import time
from typing import Callable, Optional, Tuple

class UdpSocket:
    """
    Simple multicast UDP listener/sender where payloads are always strings.

    handler signature:
        handler(text: str, addr: tuple, timestamp: float) -> None
    """

    def __init__(
        self,
        group: str,
        port: int,
        handler: Callable[[str, Tuple, float], None],
        iface_ip: Optional[str] = None
    ):
        self.group = group
        self.port = port
        self.handler = handler
        self.iface_ip = iface_ip

        self._sock = None
        self._thread = None
        self._stop = threading.Event()
        self._is_ipv6 = ":" in group
        self._v6_ifindex = 0

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------
    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._sock = self._setup_socket()
        self._stop.clear()
        self._thread = threading.Thread(target=self._rx_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._sock:
            try:
                self._sock.settimeout(0.1)
            except:
                pass

        if self._thread:
            self._thread.join(timeout=1.0)

        self._cleanup()

    def send(self, text: str, dest: Optional[Tuple] = None):
        """
        Send a string (UTF-8 encoded).
        If dest is None, send to the multicast (group, port).
        """
        if not self._sock:
            raise RuntimeError("UdpSocket not started")

        data = text.encode("utf-8")
        if dest is None:
            dest = self._default_dest()

        return self._sock.sendto(data, dest)

    # ---------------------------------------------------------
    # Setup
    # ---------------------------------------------------------
    def _setup_socket(self):
        family = socket.AF_INET6 if self._is_ipv6 else socket.AF_INET
        sock = socket.socket(family, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if self._is_ipv6:
            sock.bind(('::', self.port))
            mreq, ifindex = self._make_mreq_v6()
            self._v6_ifindex = ifindex
            sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
        else:
            sock.bind(('0.0.0.0', self.port))
            mreq = self._make_mreq_v4()
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        sock.settimeout(1.0)
        return sock

    def _cleanup(self):
        if not self._sock:
            return
        try:
            if self._is_ipv6:
                mreq, _ = self._make_mreq_v6()
                self._sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_LEAVE_GROUP, mreq)
            else:
                mreq = self._make_mreq_v4()
                self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
        finally:
            self._sock.close()
            self._sock = None

    # ---------------------------------------------------------
    # Receive loop
    # ---------------------------------------------------------
    def _rx_loop(self):
        sock = self._sock
        while not self._stop.is_set():
            try:
                data, addr = sock.recvfrom(65535)
            except socket.timeout:
                continue
            except OSError:
                break

            text = data.decode("utf-8", errors="replace")
            ts = time.time()
            try:
                self.handler(text, addr, ts)
            except Exception:
                pass

    # ---------------------------------------------------------
    # Helper functions
    # ---------------------------------------------------------
    def _make_mreq_v4(self):
        g = socket.inet_aton(self.group)
        i = socket.inet_aton(self.iface_ip) if self.iface_ip else struct.pack("!I", socket.INADDR_ANY)
        return g + i

    def _make_mreq_v6(self):
        addr_part = self.group.split('%')[0]
        g = socket.inet_pton(socket.AF_INET6, addr_part)

        if '%' in self.group:
            ifname = self.group.split('%')[1]
            ifindex = socket.if_nametoindex(ifname)
        else:
            ifindex = 0

        mreq = g + struct.pack("@I", ifindex)
        return mreq, ifindex

    def _default_dest(self):
        if self._is_ipv6:
            return (self.group.split('%')[0], self.port, 0, self._v6_ifindex)
        return (self.group, self.port)
