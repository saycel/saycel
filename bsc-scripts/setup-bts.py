#!/usr/bin/fab -f
"""
Rhizomatica BTS Toolkit

Automate maintenance on the BTS
"""

import sys
from fabric.api import env, run, task


def ssh():
    env.user = 'root'
    env.password = ''

@task
def setup():
    ssh()
    run('sbts2050-util sbts2050-pwr-enable 1 1 0')
    run('sed -i s/NO_START=0/NO_START=1/ /etc/default/osmo-nitb')
    run('mv /etc/rc5.d/S90gprs.sh /home/root/ || true')
    run('mv /etc/rc5.d/S30osmo-bsc /etc/rc5.d/K30osmo-bsc || true')
    run('mv /etc/rc5.d/S30osmo-bsc-mgcp /etc/rc5.d/K30osmo-bsc-mgcp || true')
    run('mv /etc/rc5.d/S30osmo-nitb /etc/rc5.d/K30osmo-nitb || true')
    run('sed -i -e "s/sysmobts-2050\/201208\//sysmobts-2050\/201208-testing\//g" /etc/opkg/*')
    run('opkg remove openggsn osmo-sgsn lcr')
    run('opkg update')
    run('opkg upgrade || true')
    run('opkg upgrade')

    trx_nr = int(run('sysmobts-util trx-nr'))
    osmo(trx_nr)
    network(trx_nr)


def osmo(trx_nr):
    etc_osmo_bts = """
!
! OsmoBTS () configuration saved from vty
!!
!
log stderr
  logging color 0
  logging timestamp 0
  logging level all everything
  logging level rsl info
  logging level oml info
  logging level rll notice
  logging level rr notice
  logging level meas notice
  logging level pag info
  logging level l1c info
  logging level l1p info
  logging level dsp debug
  logging level abis notice
!
line vty
 no login
!
bts 0
  band 850
  ipa unit-id 1000 %(trx_nr)d
  oml remote-ip 172.16.0.1
    """ % {'trx_nr': trx_nr}
    run("echo '%s' > /etc/osmocom/osmo-bts.cfg" % (etc_osmo_bts,))


def network(trx_nr):
    if trx_nr == 0:
        ip = "172.16.0.11"  # master
    else:
        ip = "172.16.0.12"  # slave

    interfaces = """
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address %s
    netmask 255.255.255.0
    """ % (ip,)
    run("echo '%s' > /etc/network/interfaces" % (interfaces,))


@task(default=True)
def help():
    print "%s -H bts_ip setup" % (sys.argv[0],)

setup()