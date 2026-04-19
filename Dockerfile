# Dockerfile for unslop CLI.
#
# Build:
#   docker build -t unslop .
#
# Run (deterministic, reads from stdin):
#   cat doc.md | docker run --rm -i unslop --stdin --deterministic
#
# Run (LLM mode with Anthropic API key, file mounted in):
#   docker run --rm -it \
#     -v "$PWD":/work -w /work \
#     -e ANTHROPIC_API_KEY \
#     unslop docs/README.md
#
# The image is intentionally minimal: no Anthropic SDK preinstalled. Pass
# --build-arg INSTALL_LLM=1 to include it if you plan to use LLM mode inside
# the container.

ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim AS builder

WORKDIR /src
COPY unslop/ ./unslop/

ARG INSTALL_LLM=0
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install ./unslop \
    && if [ "${INSTALL_LLM}" = "1" ]; then \
         pip install --no-cache-dir --prefix=/install "./unslop[llm]"; \
       fi


FROM python:${PYTHON_VERSION}-slim

LABEL org.opencontainers.image.title="unslop"
LABEL org.opencontainers.image.description="Strip AI-isms from markdown/text; preserve code, URLs, and headings."
LABEL org.opencontainers.image.source="https://github.com/MohamedAbdallah-Hu/unslop"
LABEL org.opencontainers.image.licenses="MIT"

RUN groupadd --system humanize && useradd --system --gid humanize --no-create-home humanize
USER humanize
WORKDIR /work

COPY --from=builder /install /usr/local

ENTRYPOINT ["unslop"]
CMD ["--help"]
