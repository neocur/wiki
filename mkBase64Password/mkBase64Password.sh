#!/bin/bash
for i in {1..10}
do
    KEY_HEX=$(openssl rand -hex 32)
    KEY_B64=$(echo $KEY_HEX | xxd -r -p | base64 )
    if [[ ! $KEY_B64 =~ "+" ]] && [[ ! $KEY_B64 =~ "/" ]]; then
        KEY_ENC=$(echo $KEY_HEX | xxd -r -p )
        break
    fi
done
if [ $i -eq 10 ]; then
    exit 0
fi
    

echo Password: $KEY_B64
echo $KEY_HEX | xxd -r -p > __temp_key
openssl aes-128-cbc -e -iter 3 -in __temp_key -out __temp_key_crypted
cat __temp_key_crypted | base64 -w 44 > key
rm -f __temp_key __temp_key_crypted
