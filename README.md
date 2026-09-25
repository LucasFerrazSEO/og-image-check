**English** · [Português (Brasil)](README.pt-BR.md)

# og-image-check

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)

`og-image-check` is a free, open source command-line tool that checks
whether a URL's `og:image` exists and measures its real width and height.
It tells you whether the image meets the recommended minimum (1200px wide)
before it shows up cropped or pixelated when shared on WhatsApp, LinkedIn
or anywhere else that renders a link card. It uses the Python standard
library only.

## Contents

- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [FAQ](#faq)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

## How it works

1. Fetches the given URL and extracts the `og:image` value (falls back to
   `twitter:image` if `og:image` is missing).
2. Downloads the image and parses the binary header (PNG, JPEG, GIF and
   WEBP) to get the real width and height, without any image library such
   as Pillow.
3. Compares the width against the given minimum.

## Requirements

Python 3.9 or newer. Standard library only (uses `urllib` and `struct`),
no external dependencies.

## Installation

```bash
git clone https://github.com/LucasFerrazSEO/og-image-check.git
cd og-image-check
```

## Usage

The tool prints its report in Brazilian Portuguese.

**1. Point it at the URL of the page you want to test.**

```bash
python og_image_check.py https://exemplo.com/pagina/
```

**2. Read the result.** Sample output for an image that meets the
recommended minimum:

```
=== og-image-check: https://exemplo.com/pagina/ ===

Imagem: https://exemplo.com/img/capa.jpg
Dimensões: 1200x630px
ok  largura >= 1200px
```

And for an image below the minimum:

```
=== og-image-check: https://exemplo.com/outra-pagina/ ===

Imagem: https://exemplo.com/img/pequena.jpg
Dimensões: 600x315px
ATENÇÃO  largura abaixo do mínimo recomendado de 1200px
```

**3. Change the required minimum** if your editorial standard is different
from 1200px:

```bash
python og_image_check.py https://exemplo.com/pagina/ --minimo 1080
```

**4. Run it in batch**, checking several URLs at once with a shell loop:

```bash
for u in https://exemplo.com/a/ https://exemplo.com/b/; do
  python og_image_check.py "$u"
done
```

## FAQ

**Is og-image-check really free?**
Yes. It is open source under the MIT license.

**Why 1200px wide as the default?**
It is the minimum most often cited by the platforms (Facebook/Meta,
LinkedIn) to avoid cropping or blurring in the share card. It is not a
universal number guaranteed by every platform, which is why the minimum is
adjustable.

**Does it work with AVIF images?**
Not in this version. It covers PNG, JPEG, GIF and WEBP, the most common
formats in `og:image` today.

**Does the tool download the whole page?**
It downloads the page HTML (to find the tag) and then the image itself, to
read the real dimensions of the file.

## Limitations

No JavaScript execution. If the `og:image` tag is built with JavaScript in
the browser, this script does not see it (the same reading limit most
share crawlers have). It covers PNG, JPEG, GIF and WEBP. AVIF dimension
parsing is not implemented here.

## Contributing

Bug reports and suggestions are welcome through [GitHub Issues](https://github.com/LucasFerrazSEO/og-image-check/issues).

## Author

[Lucas Ferraz](https://lucasferraz.com) is an SEO, website development and Generative Engine Optimization specialist and the founder of [Lucas Ferraz SEO](https://lucasferrazseo.com).

## License

MIT. See [LICENSE](LICENSE).
