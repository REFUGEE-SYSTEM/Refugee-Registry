FROM openg2p/iam-staff-portal-api:1.3.0

USER root
RUN pip install --no-cache-dir psycopg2-binary minio

COPY iam_registration_payload.json /opt/bootstrap/iam_registration_payload.json
COPY bootstrap.py /opt/bootstrap/bootstrap.py

ENTRYPOINT ["python3", "/opt/bootstrap/bootstrap.py"]
