#!/usr/bin/env python3
"""Regression for real CLI notices; never hide an API error or arbitrary prefix."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('cloud',Path(__file__).parent/'live/cloud.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert m.decode_response('{"volume": {}}')=={'volume':{}}
assert m.decode_response('可执行`hcloud update`更新KooCLI至最新版本7.3.12\n{"volume": {}}')=={'volume':{}}
assert m.decode_response('{"error_code":"DENIED"}')=={'error_code':'DENIED'}
for value in ['[OPENAPI_ERROR] failed\n{"volume":{}}','unexpected warning\n{"volume":{}}','[]','{"volume":{}}\nerror']:
 try:m.decode_response(value)
 except ValueError:pass
 else:raise AssertionError('Accepted invalid prefix or response')
print('PASS 7 CLI response cases')
