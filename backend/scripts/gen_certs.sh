#!/bin/bash

# Commands from https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/configuring-https-ssl.html

echo 'Generating RSA private key...'
openssl genrsa 2048 > private.key

echo 'Creating CSR...'
openssl req -new -key private.key -out csr.pem -subj "/C=XX/ST=XX/L=XX/O=XX/OU=XX/CN=XX/emailAddress=XX"

# NOTE self-signed cert currently does not work in application
echo 'Creating self-signed public certificate...'
openssl x509 -req -days 365 -in csr.pem -signkey private.key -out public.crt
