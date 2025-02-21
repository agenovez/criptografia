#!/bin/bash
# Script para generar certificados RSA, firmar y verificar documentos con OpenSSL

# Configuración de contraseñas
CA_PASSWORD="password"
USER_PASSWORD="password"

# Crear Directorios
mkdir -p certs && cd certs

# 1️⃣ Generar la Autoridad Certificadora (CA)
echo "🔹 Generando la Autoridad Certificadora (CA)"
openssl genpkey -algorithm RSA -out ca.key -aes256 -pass pass:$CA_PASSWORD
openssl req -new -x509 -key ca.key -sha256 -days 3650 -out ca.crt -subj "/CN=MiCA" -passin pass:$CA_PASSWORD

# 2️⃣ Generar claves RSA para el usuario y certificado
echo "🔹 Generando clave privada del usuario"
openssl genpkey -algorithm RSA -out user.key -aes256 -pass pass:$USER_PASSWORD
openssl req -new -key user.key -out user.csr -subj "/CN=Usuario" -passin pass:$USER_PASSWORD
openssl x509 -req -in user.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out user.crt -days 365 -sha256 -passin pass:$CA_PASSWORD

# 3️⃣ Firmar un documento
echo "🔹 Creando y firmando un documento"
echo "Este es un documento importante." > documento.txt
openssl dgst -sha256 -sign user.key -out documento.sig documento.txt -passin pass:$USER_PASSWORD

# 4️⃣ Verificar la firma
echo "🔹 Verificando la firma"
openssl dgst -sha256 -verify <(openssl x509 -in user.crt -pubkey -noout) -signature documento.sig documento.txt

# 5️⃣ Verificar el certificado del usuario
echo "🔹 Verificando la validez del certificado"
openssl verify -CAfile ca.crt user.crt

echo "✅ Proceso completado exitosamente!"
