# Estación de explotación de binarios (pwn) para la Parte 5.
# Compila binarios DELIBERADAMENTE vulnerables (de laboratorio) con las protecciones
# desactivadas, para practicar análisis y explotación en un entorno aislado y propio.
FROM debian:12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc gdb python3 python3-pip file gcc-multilib \
        ltrace strace vim less \
    && rm -rf /var/lib/apt/lists/*

# pwntools (framework de explotación) en un entorno virtual.
RUN pip3 install --break-system-packages --no-cache-dir pwntools

WORKDIR /pwn
COPY reto1_overflow.c build.sh ./
RUN chmod +x build.sh && ./build.sh

CMD ["sleep", "infinity"]
