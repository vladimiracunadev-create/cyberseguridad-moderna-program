# Estación de análisis forense de memoria (Volatility 3 + YARA).
# Para los labs de forense de memoria y malware para IR (clases 207, 325, 326).
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
        file \
    && rm -rf /var/lib/apt/lists/*

# Volatility 3 (framework de forense de memoria) + YARA para escaneo de reglas.
RUN pip install --no-cache-dir volatility3 yara-python capstone pefile

WORKDIR /cases
CMD ["sleep", "infinity"]
