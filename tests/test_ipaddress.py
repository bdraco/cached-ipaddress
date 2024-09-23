"""Unit tests for cached_ipaddress.ipaddress."""

from ipaddress import IPv4Address, IPv6Address

from cached_ipaddress import ipaddress


def test_cached_ip_addresses_wrapper():
    """Test the cached_ip_addresses_wrapper."""
    assert ipaddress.cached_ip_addresses("") is None
    assert ipaddress.cached_ip_addresses("foo") is None
    assert (
        str(
            ipaddress.cached_ip_addresses(
                b"&\x06(\x00\x02 \x00\x01\x02H\x18\x93%\xc8\x19F"
            )
        )
        == "2606:2800:220:1:248:1893:25c8:1946"
    )
    assert ipaddress.cached_ip_addresses("::1") == ipaddress.IPv6Address("::1")

    ipv4 = ipaddress.cached_ip_addresses("169.254.0.0")
    assert ipv4 is not None
    assert ipv4.is_link_local is True
    assert ipv4.is_unspecified is False
    assert ipv4.is_loopback is False
    assert str(ipv4) == "169.254.0.0"
    assert str(ipv4) == "169.254.0.0"
    assert ipv4.reverse_pointer == "0.0.254.169.in-addr.arpa"

    ipv4 = ipaddress.cached_ip_addresses("0.0.0.0")  # noqa: S104
    assert ipv4 is not None
    assert ipv4.is_link_local is False
    assert ipv4.is_unspecified is True
    assert ipv4.is_loopback is False
    assert ipv4.is_multicast is False
    assert ipv4.compressed == IPv4Address(str(ipv4)).compressed

    ipv6 = ipaddress.cached_ip_addresses("fe80::1")
    assert ipv6 is not None
    assert ipv6.is_link_local is True
    assert ipv6.is_unspecified is False
    assert ipv6.is_loopback is False
    assert ipv6.is_multicast is False
    assert (
        ipv6.reverse_pointer
        == "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.e.f.ip6.arpa"
    )

    ipv6 = ipaddress.cached_ip_addresses("0:0:0:0:0:0:0:0")
    assert ipv6 is not None
    assert ipv6.is_link_local is False
    assert ipv6.is_unspecified is True
    assert ipv6.is_loopback is False
    assert str(ipv6) == "::"

    assert hash(ipv4) == hash(IPv4Address(str(ipv4)))
    assert hash(ipv6) == hash(IPv6Address(str(ipv6)))
    assert int(ipv4) == int(IPv4Address(str(ipv4)))
    assert int(ipv6) == int(IPv6Address(str(ipv6)))
    assert ipv6.compressed == IPv6Address(str(ipv6)).compressed
