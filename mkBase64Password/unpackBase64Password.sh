#!/bin/bash

base64 -d > ./__temp_key_crypted
openssl aes-128-cbc -d -iter 3 -in ./__temp_key_crypted -out ./__temp_key
cat ./__temp_key | base64
rm -f ./__temp_key_crypted ./__temp_key

