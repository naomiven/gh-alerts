#!/bin/bash

aws iam upload-server-certificate --server-certificate-name gh-alerts-server-cert --certificate-body file://public.crt --private-key file://private.key
