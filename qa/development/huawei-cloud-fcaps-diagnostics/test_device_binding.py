#!/usr/bin/env python3
"""Ambiguous identifiers and other disk buses must not acquire a false binding."""
import importlib.util,copy
from pathlib import Path
s=importlib.util.spec_from_file_location('binding',Path(__file__).parent/'live/device_binding.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
vid='12345678-1234-1234-1234-123456789abc';prefix=vid[:20]
a=[{'volumeId':vid,'bus':'virtio','pciAddress':'0000:02:01.0'}]
d=[{'DEVNAME':'/dev/vda','DEVTYPE':'disk','ID_SERIAL':prefix,'DEVPATH':'/devices/pci/virtio3/block/vda','ID_PATH':'pci-0000:02:01.0'}]
assert m.bind_virtio(vid,a,d)=='/dev/vda'
tests=[]
x=copy.deepcopy(a);x[0]['bus']='scsi';tests.append((x,d))
tests.append((a+[{'volumeId':prefix+'ffffffffffff','bus':'virtio'}],d))
tests.append((a,d+copy.deepcopy(d)))
x=copy.deepcopy(d);x[0]['DEVTYPE']='partition';tests.append((a,x))
x=copy.deepcopy(d);x[0]['ID_PATH']='pci-0000:03:01.0';tests.append((a,x))
x=copy.deepcopy(d);x[0]['ID_SERIAL']=prefix[:-1];tests.append((a,x))
for x,y in tests:
 try:m.bind_virtio(vid,x,y)
 except ValueError:pass
 else:raise AssertionError('Accepted ambiguous or incompatible device identity')
print('PASS exact mapping and 6 rejected device-binding errors')
