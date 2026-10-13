# Formal artifact payload

`orbita_language_limit_lean_v0_1.zip.b64` is the Base64 encoding of the exact Lean ZIP supplied for this audit.

Expected reconstructed ZIP SHA-256:

`3ff0a2bf1034a34111f5060bdafe947daf46c3245f6a894d55a168b700b2409c`

Reconstruct locally:

```bash
base64 -d artifacts/orbita_language_limit_lean_v0_1.zip.b64 > /tmp/orbita_language_limit_lean_v0_1.zip
echo "3ff0a2bf1034a34111f5060bdafe947daf46c3245f6a894d55a168b700b2409c  /tmp/orbita_language_limit_lean_v0_1.zip" | sha256sum -c -
unzip /tmp/orbita_language_limit_lean_v0_1.zip -d /tmp/orbita-lean
cd /tmp/orbita-lean/orbita_language_limit_lean
lake update
lake exe cache get
lake build
```

The archive pins Lean and Mathlib to v4.32.1. CI performs the same reconstruction and build.
