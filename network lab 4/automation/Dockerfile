FROM python:3.10-alpine
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev curl iproute2
RUN pip install python-dotenv requests cryptography
WORKDIR /automation