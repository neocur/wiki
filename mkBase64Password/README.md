# Password transported with encryption AES

## HOW TO

### 1. Make 32-byte Base64 Password
```bash
$ ./mkBase64Password
Password: ieRvnzp5a14GSrq+VmjrSlL/7I3Px22NuDqSHHMgOhI=	// Use this password
enter aes-128-cbc encryption password:
Verifying - enter aes-128-cbc encryption password:

```

Use a file named key, which is encrypted, to transport by email or QR code and
a base64-output for password.

### 2. Unpack encrypted Base64 string to get password
```bash
$ cat key | ./unpackBase64Password
enter aes-128-cbc decryption password:
ieRvnzp5a14GSrq+VmjrSlL/7I3Px22NuDqSHHMgOhI= 

```

Yes. It is the password.



