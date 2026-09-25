#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
og-image-check — confere se a `og:image` de uma URL existe e mede sua
largura e altura reais, para saber se ela cumpre o mínimo recomendado
(1200px de largura) antes de a imagem aparecer cortada ou pixelada em um
compartilhamento.

O QUE FAZ
    1. Busca a URL informada e extrai o valor de `og:image` (e
       `twitter:image` como alternativa, se `og:image` faltar).
    2. Baixa só os primeiros bytes necessários da imagem (lê em pedaços até
       achar o cabeçalho de dimensão, sem baixar o arquivo inteiro quando
       possível) e faz o parsing binário do formato — PNG, JPEG, GIF e WEBP
       — para extrair largura e altura reais, sem depender de nenhuma
       biblioteca de imagem (Pillow, etc).
    3. Compara a largura contra o mínimo informado (padrão 1200px).

USO
    python og_image_check.py https://exemplo.com/pagina/
    python og_image_check.py https://exemplo.com/pagina/ --minimo 1200

LIMITAÇÕES
    Só biblioteca padrão (`urllib`), sem execução de JavaScript — se a
    página monta a tag `og:image` via JavaScript no navegador, este script
    não vê. Cobre PNG, JPEG, GIF e WEBP (os formatos usados hoje em
    og:image); AVIF não tem parsing de dimensão aqui.

Autor: Lucas Ferraz (lucasferraz.com) — dependência zero, só biblioteca padrão.
Licença: MIT.
"""
from __future__ import annotations

import argparse
import re
import struct
import sys
import urllib.error
import urllib.request

UA = {"User-Agent": "og-image-check/1.0 (+https://github.com/lucasferrazseo/og-image-check)"}
META_RE = re.compile(
    r'(?is)<meta\s+[^>]*(?:property|name)=["\']({prop})["\'][^>]*content=["\']([^"\']+)["\']'
)


def busca_texto(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def busca_bytes(url: str, limite: int = 2_000_000) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read(limite)


def extrai_meta(html: str, prop: str) -> str:
    padrao = re.compile(META_RE.pattern.format(prop=re.escape(prop)), re.I | re.S)
    m = padrao.search(html)
    return m.group(2) if m else ""


def dimensoes_png(dados: bytes) -> tuple[int, int] | None:
    if dados[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    largura, altura = struct.unpack(">II", dados[16:24])
    return largura, altura


def dimensoes_gif(dados: bytes) -> tuple[int, int] | None:
    if dados[:6] not in (b"GIF87a", b"GIF89a"):
        return None
    largura, altura = struct.unpack("<HH", dados[6:10])
    return largura, altura


def dimensoes_jpeg(dados: bytes) -> tuple[int, int] | None:
    if dados[:2] != b"\xff\xd8":
        return None
    i = 2
    tamanho = len(dados)
    while i < tamanho - 1:
        if dados[i] != 0xFF:
            i += 1
            continue
        marcador = dados[i + 1]
        if marcador in (0xD8, 0xD9):
            i += 2
            continue
        if i + 4 > tamanho:
            break
        comprimento_bloco = struct.unpack(">H", dados[i + 2:i + 4])[0]
        if 0xC0 <= marcador <= 0xCF and marcador not in (0xC4, 0xC8, 0xCC):
            if i + 9 > tamanho:
                break
            altura, largura = struct.unpack(">HH", dados[i + 5:i + 9])
            return largura, altura
        i += 2 + comprimento_bloco
    return None


def dimensoes_webp(dados: bytes) -> tuple[int, int] | None:
    if dados[:4] != b"RIFF" or dados[8:12] != b"WEBP":
        return None
    fourcc = dados[12:16]
    if fourcc == b"VP8 ":
        largura, altura = struct.unpack("<HH", dados[26:30])
        return largura & 0x3FFF, altura & 0x3FFF
    if fourcc == b"VP8L":
        b = dados[21:25]
        bits = int.from_bytes(b, "little")
        largura = (bits & 0x3FFF) + 1
        altura = ((bits >> 14) & 0x3FFF) + 1
        return largura, altura
    if fourcc == b"VP8X":
        largura = int.from_bytes(dados[24:27], "little") + 1
        altura = int.from_bytes(dados[27:30], "little") + 1
        return largura, altura
    return None


def dimensoes(dados: bytes) -> tuple[int, int] | None:
    for parser in (dimensoes_png, dimensoes_gif, dimensoes_jpeg, dimensoes_webp):
        resultado = parser(dados)
        if resultado:
            return resultado
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description="Confere existência e dimensões da og:image de uma URL.")
    ap.add_argument("url", help="URL da página")
    ap.add_argument("--minimo", type=int, default=1200, help="largura mínima recomendada em px (padrão 1200)")
    args = ap.parse_args()

    try:
        html = busca_texto(args.url)
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"Falha ao buscar {args.url}: {exc}", file=sys.stderr)
        sys.exit(1)

    imagem_url = extrai_meta(html, "og:image") or extrai_meta(html, "twitter:image")
    if not imagem_url:
        print(f"\n=== og-image-check: {args.url} ===\n")
        print("ATENÇÃO  nenhuma tag og:image nem twitter:image encontrada")
        sys.exit(1)

    if imagem_url.startswith("//"):
        imagem_url = "https:" + imagem_url

    print(f"\n=== og-image-check: {args.url} ===\n")
    print(f"Imagem: {imagem_url}")

    try:
        dados = busca_bytes(imagem_url)
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"ATENÇÃO  não consegui baixar a imagem: {exc}")
        sys.exit(1)

    dim = dimensoes(dados)
    if not dim:
        print("ATENÇÃO  imagem baixada, mas não consegui ler as dimensões "
              "(formato não suportado por este script, ou arquivo corrompido)")
        sys.exit(1)

    largura, altura = dim
    print(f"Dimensões: {largura}x{altura}px")
    if largura >= args.minimo:
        print(f"ok  largura >= {args.minimo}px")
        sys.exit(0)
    print(f"ATENÇÃO  largura abaixo do mínimo recomendado de {args.minimo}px")
    sys.exit(1)


if __name__ == "__main__":
    main()
