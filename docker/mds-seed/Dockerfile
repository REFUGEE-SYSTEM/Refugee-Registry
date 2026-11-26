FROM python:3.11-slim

ARG OPENG2P_DATA_SHA=302ac29c91c87b32ceb80d6da1e04043cbc82d92

RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir psycopg2-binary boto3

RUN git init /opt/openg2p-data \
    && git -C /opt/openg2p-data remote add origin https://github.com/OpenG2P/openg2p-data.git \
    && git -C /opt/openg2p-data config core.sparseCheckout true \
    && echo "packs/ETH/" > /opt/openg2p-data/.git/info/sparse-checkout \
    && git -C /opt/openg2p-data fetch --depth=1 origin "${OPENG2P_DATA_SHA}" \
    && git -C /opt/openg2p-data checkout FETCH_HEAD \
    && rm -rf /opt/openg2p-data/.git

COPY migrations/ /opt/mds-seed/migrations/
COPY load_geo_pack.py /opt/mds-seed/load_geo_pack.py
COPY entrypoint.sh /opt/mds-seed/entrypoint.sh
RUN chmod +x /opt/mds-seed/entrypoint.sh

ENTRYPOINT ["/opt/mds-seed/entrypoint.sh"]
