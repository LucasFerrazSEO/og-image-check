[English](README.md) · **Português (Brasil)**

# og-image-check

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)

`og-image-check` é uma ferramenta de linha de comando gratuita e de código
aberto que confere se a `og:image` de uma URL existe e mede sua largura e
altura reais. Ela mostra se a imagem cumpre o mínimo recomendado (1200px
de largura) antes de aparecer cortada ou pixelada em um compartilhamento
no WhatsApp, no LinkedIn ou em qualquer outro lugar que renderize um card
de link. Usa só a biblioteca padrão do Python.

## Sumário

- [Como funciona](#como-funciona)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Perguntas frequentes](#perguntas-frequentes)
- [Limitações](#limitações)
- [Como contribuir](#como-contribuir)
- [Autor](#autor)
- [Licença](#licença)

## Como funciona

1. Busca a URL informada e extrai o valor de `og:image` (usa
   `twitter:image` como alternativa se `og:image` faltar).
2. Baixa a imagem e faz o parsing binário do cabeçalho (PNG, JPEG, GIF e
   WEBP) para extrair a largura e a altura reais, sem depender de nenhuma
   biblioteca de imagem como Pillow.
3. Compara a largura contra o mínimo informado.

## Requisitos

Python 3.9 ou mais recente. Só biblioteca padrão (usa `urllib` e
`struct`), sem dependência externa.

## Instalação

```bash
git clone https://github.com/LucasFerrazSEO/og-image-check.git
cd og-image-check
```

## Uso

**1. Aponte para a URL da página que você quer testar.**

```bash
python og_image_check.py https://exemplo.com/pagina/
```

**2. Leia o resultado.** Saída de exemplo, com uma imagem que passa no
mínimo recomendado:

```
=== og-image-check: https://exemplo.com/pagina/ ===

Imagem: https://exemplo.com/img/capa.jpg
Dimensões: 1200x630px
ok  largura >= 1200px
```

E de uma imagem abaixo do mínimo:

```
=== og-image-check: https://exemplo.com/outra-pagina/ ===

Imagem: https://exemplo.com/img/pequena.jpg
Dimensões: 600x315px
ATENÇÃO  largura abaixo do mínimo recomendado de 1200px
```

**3. Ajuste o mínimo exigido**, se seu padrão editorial for diferente de
1200px:

```bash
python og_image_check.py https://exemplo.com/pagina/ --minimo 1080
```

**4. Use em lote**, checando várias URLs de uma vez com um laço de shell:

```bash
for u in https://exemplo.com/a/ https://exemplo.com/b/; do
  python og_image_check.py "$u"
done
```

## Perguntas frequentes

**og-image-check é realmente grátis?**
Sim, código aberto sob licença MIT.

**Por que 1200px de largura como padrão?**
É o mínimo mais citado pelas plataformas (Facebook/Meta, LinkedIn) para
evitar corte ou desfoque no card de compartilhamento. Não é um número
universal garantido por todas as plataformas, por isso o mínimo é
ajustável.

**Funciona com imagem em AVIF?**
Não nesta versão. Cobre PNG, JPEG, GIF e WEBP, que são os formatos mais
comuns em `og:image` hoje.

**A ferramenta baixa a página inteira?**
Baixa o HTML da página (para achar a tag) e depois a imagem em si, para
ler as dimensões reais do arquivo.

## Limitações

Sem execução de JavaScript. Se a tag `og:image` é montada via JavaScript
no navegador, este script não vê (o mesmo limite de leitura que a maioria
dos crawlers de compartilhamento também tem). Cobre PNG, JPEG, GIF e WEBP.
AVIF não tem parsing de dimensão implementado aqui.

## Como contribuir

Relatos de erro e sugestões são bem-vindos pelas [Issues do GitHub](https://github.com/LucasFerrazSEO/og-image-check/issues).

## Autor

[Lucas Ferraz](https://lucasferraz.com) é especialista em SEO, criação de sites e Generative Engine Optimization e fundador da [Lucas Ferraz SEO](https://lucasferrazseo.com).

## Licença

MIT. Veja o arquivo [LICENSE](LICENSE).
