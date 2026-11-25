ARG RP_VERSION=0.0.0-develop.716
FROM openg2p/openg2p-registry-db-seed:${RP_VERSION}

RUN rm -rf /seed/meta_data/* /seed/awe_meta_data/* /seed/templates/* /seed/seed-data/*

COPY refugee-extension/src/openg2p_registry_refugee_extension/meta_data/     /seed/meta_data/
COPY refugee-extension/src/openg2p_registry_refugee_extension/awe_meta_data/ /seed/awe_meta_data/
COPY refugee-extension/src/openg2p_registry_refugee_extension/templates/     /seed/templates/

COPY docker/db-seed/load_sample_data.py /seed/load_sample_data.py
RUN chmod +x /seed/load_sample_data.py

COPY docker/db-seed/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
