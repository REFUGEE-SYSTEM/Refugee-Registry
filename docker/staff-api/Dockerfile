ARG RP_VERSION=0.0.0-develop.716
FROM openg2p/openg2p-registry-staff-api:${RP_VERSION}

# Compatibility shim: iam-core 1.4.0 expects openg2p_fastapi_common.utils.crypto, which moved to .crypto in 1.2.1
RUN python3 -c "import pathlib, openg2p_fastapi_common as c; p = pathlib.Path(c.__file__).parent / 'utils'; p.mkdir(exist_ok=True); (p / '__init__.py').write_text('from openg2p_fastapi_common import crypto\n'); (p / 'crypto.py').write_text('from openg2p_fastapi_common.crypto import *\nfrom openg2p_fastapi_common.crypto import CryptoHelper\n')"

ENV REGISTRY_EXTENSION_MODULE=openg2p_registry_refugee_extension

COPY refugee-extension/ /app/refugee-extension/
RUN pip install --no-cache-dir /app/refugee-extension
