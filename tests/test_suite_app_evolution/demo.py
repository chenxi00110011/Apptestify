from tplinkrouterc6u import (
    TplinkRouterProvider,
    TplinkRouter,
    TplinkC1200Router,
    TPLinkMRClient,
    TPLinkDecoClient,
    Connection
)
from logging import Logger

router = TplinkRouterProvider.get_client('http://192.168.1.1', 'cx123456')
# You may use client directly like router = TplinkRouter('http://192.168.0.1', 'password') You may also pass username
# if it is different and a logger to log errors as router = TplinkRouter('http://192.168.0.1','password','admin2',
# Logger('test')) If you have the TP-link C1200 V2 or similar, you can use the TplinkC1200Router class instead of the
# TplinkRouter class. Remember that the password for this router is different, here you need to use the web encrypted
# password. To get web encrypted password, read Web Encrypted Password section router = TplinkC1200Router(
# 'http://192.168.0.1','WebEncryptedPassword', Logger('test'))
router.reboot()
try:
    router.authorize()  # authorizing
    # Get firmware info - returns Firmware
    firmware = router.get_firmware()

    # Get status info - returns Status
    status = router.get_status()
    if not status.guest_2g_enable:  # check if guest 2.4G wifi is disable
        router.set_wifi(Connection.GUEST_2G, True)  # turn on guest 2.4G wifi

    # Get Address reservations, sort by ipaddr
    reservations = router.get_ipv4_reservations()
    reservations.sort(key=lambda a: a.ipaddr)
    for res in reservations:
        print(f"{res.macaddr} {res.ipaddr:16s} {res.hostname:36} {'Permanent':12}")

    # Get DHCP leases, sort by ipaddr
    leases = router.get_ipv4_dhcp_leases()
    leases.sort(key=lambda a: a.ipaddr)
    for lease in leases:
        print(f"{lease.macaddr} {lease.ipaddr:16s} {lease.hostname:36} {lease.lease_time:12}")
finally:
    router.logout()  # always logout as TP-Link Web Interface only supports upto 1 user logged