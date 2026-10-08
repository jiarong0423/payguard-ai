"""Fail-closed stdlib inventory guard; never create an SDK context/client/tool."""
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import sys
import tomllib

PINNED_DIRECT = {'paypal-agent-toolkit':'1.11.0','openai-agents':'0.0.2','openai':'1.66.0','mem0ai':'0.1.116','fastapi':'0.142.2','uvicorn':'0.54.0','httpx':'0.28.1'}
PROJECT_MARKERS = {'tools/public_run.sh':'452a7b3c7739b600cc53050afa2ef5a25990f5eef4ef4f44cf532c6127c88fe2','backend/app/paypal_tools.py':'303cca1765c1f278c370fc28b981828f6b2ec2b4c0272c13a5dc4f7f65cd7ecc','src/payguard/__init__.py':'3b53b18a8fb37bcea80ed7910e4a49d4f437086bc5474e76f0ed39904948758c'}
EXPECTED_LOCK_SHA256 = 'ed2392d04d2b06e59e990e6cd84d49b6754f251d03c2756ad7814fc805d23593'
TOOLKIT_WHEEL_SHA256 = '207614c35541426405466620c96c554de9d980d558a9fd2cd1ed86cc3ffcc06c'

class RuntimeRejected(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)

def reject(code):
    raise RuntimeRejected(code)

def normalize(name):
    return re.sub(r'[-_.]+','-',name.lower())

def parse_lock(raw):
    if type(raw) is not bytes or not 0 < len(raw) <= 2000000:
        reject('PROFILE_LOCK_INVALID')
    try:
        lines = raw.decode('utf-8').splitlines()
    except UnicodeError:
        reject('PROFILE_LOCK_INVALID')
    pins = {}; hashes = {}; current = None
    for line in lines:
        if not line.strip() or line.lstrip().startswith('#'):
            reject('PROFILE_LOCK_INVALID')
        pin = re.fullmatch(r'([a-z0-9][a-z0-9_.-]*)==([0-9][a-zA-Z0-9.!+_-]*) \\',line)
        if pin:
            if current is not None and not hashes[current]: reject('PROFILE_LOCK_INVALID')
            current = normalize(pin[1])
            if current in pins: reject('PROFILE_LOCK_INVALID')
            pins[current] = pin[2]; hashes[current] = []
        else:
            digest = re.fullmatch(r'    --hash=sha256:([a-f0-9]{64})(?: \\)?',line)
            if not digest or current is None or digest[1] in hashes[current]: reject('PROFILE_LOCK_INVALID')
            hashes[current].append(digest[1])
    if len(pins) != 160 or any(not values for values in hashes.values()): reject('PROFILE_LOCK_INVALID')
    if hashes.get('paypal-agent-toolkit') != [TOOLKIT_WHEEL_SHA256]: reject('PROFILE_TOOLKIT_HASH_INVALID')
    return pins

def validate_profile(profile):
    try:
        raw = (profile/'requirements.lock').read_bytes()
        manifest = tomllib.loads((profile/'pyproject.toml').read_text(encoding='utf-8'))
    except (OSError,ValueError,UnicodeError):
        reject('PROFILE_MANIFEST_INVALID')
    tool = manifest.get('tool',{}).get('payguard-paypal-toolkit',{})
    project = manifest.get('project',{})
    if not isinstance(tool,dict) or not isinstance(project,dict): reject('PROFILE_MANIFEST_INVALID')
    actual_hash = hashlib.sha256(raw).hexdigest()
    if actual_hash != EXPECTED_LOCK_SHA256 or tool.get('lock-sha256') != actual_hash: reject('PROFILE_LOCK_HASH_INVALID')
    if project.get('requires-python') != '==3.12.*' or type(tool.get('inventory-count')) is not int or tool['inventory-count'] != 160 or tool.get('tracing') != 'disabled' or tool.get('project-markers') != PROJECT_MARKERS: reject('PROFILE_MANIFEST_INVALID')
    dependencies = project.get('dependencies')
    if not isinstance(dependencies,list) or sorted(dependencies) != sorted(f'{name}=={version}' for name,version in PINNED_DIRECT.items()): reject('PROFILE_MANIFEST_INVALID')
    pins = parse_lock(raw)
    if any(pins.get(name) != version for name,version in PINNED_DIRECT.items()): reject('PROFILE_MANIFEST_INVALID')
    return pins

def validate_inventory(pins, distributions):
    installed = {}
    for distribution in distributions:
        name = distribution.metadata.get('Name')
        if not isinstance(name,str) or not name: reject('PROFILE_INVENTORY_INVALID')
        name = normalize(name)
        if name in installed: reject('PROFILE_INVENTORY_INVALID')
        installed[name] = distribution.version
    if installed != pins: reject('PROFILE_INVENTORY_MISMATCH')

def validate_project_root(root):
    try:
        for relative, digest in PROJECT_MARKERS.items():
            if hashlib.sha256((root/relative).read_bytes()).hexdigest() != digest: reject('PROFILE_PROJECT_MISMATCH')
        if not (root/'tests/test_paypal_tools.py').is_file(): reject('PROFILE_PROJECT_MISMATCH')
    except OSError:
        reject('PROFILE_PROJECT_MISMATCH')
    return root

def validate_project(profile):
    # Formal canonical and exported layouts share this exact stable marker path.
    # No ancestor search, arbitrary caller project root, or root runtime fallback.
    return validate_project_root(profile.parent.parent)

def import_capabilities(root):
    sys.path[:0] = [str(root/'src'),str(root/'backend')]
    try:
        from agents import FunctionTool, set_tracing_disabled
        set_tracing_disabled(True)
        from app.paypal_tools import SafePaypalToolGateway, create_official_invoice_tool
        if not isinstance(FunctionTool,type) or not isinstance(SafePaypalToolGateway,type) or not callable(create_official_invoice_tool): reject('PROFILE_IMPORT_UNAVAILABLE')
    except RuntimeRejected:
        raise
    except Exception:
        reject('PROFILE_IMPORT_UNAVAILABLE')

def check(profile, *, version=None, distributions=None, capability_loader=None):
    version = sys.version_info if version is None else version
    if tuple(version[:2]) != (3,12): reject('PROFILE_PYTHON_312_REQUIRED')
    pins = validate_profile(profile)
    validate_inventory(pins,importlib.metadata.distributions() if distributions is None else distributions)
    root = validate_project(profile)
    (import_capabilities if capability_loader is None else capability_loader)(root)
    return {'status':'PROFILE_READY','python':'.'.join(str(x) for x in version[:3]),'locked_distributions':160,'tracing':'disabled','gateway':'SafePaypalToolGateway','sdk_executor':'NOT_USED'}

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        print('PROFILE_ARGUMENTS_REJECTED',file=sys.stderr); return 64
    try:
        result = check(Path(__file__).resolve().parent)
    except RuntimeRejected as failure:
        print(failure.code,file=sys.stderr); return 78
    except Exception:
        print('PROFILE_RUNTIME_UNAVAILABLE',file=sys.stderr); return 78
    print(json.dumps(result,sort_keys=True)); return 0

if __name__ == '__main__':
    raise SystemExit(main())
