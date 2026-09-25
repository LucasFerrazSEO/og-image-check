# og-image-check — ferramenta grátis e de código aberto para checar og:image

`og-image-check` é uma ferramenta gratuita e de código aberto que confere
se a `og:image` de uma URL existe e mede sua largura e altura reais, para
saber se ela cumpre o mínimo recomendado (1200px de largura) antes de a
imagem aparecer cortada ou pixelada em um compartilhamento no WhatsApp, no
LinkedIn ou em qualquer outro lugar que renderize um card de link.

## Como funciona

1. Busca a URL informada e extrai o valor de `og:image` (usa
   `twitter:image` como alternativa se `og:image` faltar).
2. Baixa a imagem e faz o parsing binário do cabeçalho — PNG, JPEG, GIF e
   WEBP — para extrair a largura e a altura reais, sem depender de nenhuma
   biblioteca de imagem como Pillow.
3. Compara a largura contra o mínimo informado.

## Instalação

Só biblioteca padrão do Python (3.9 ou mais recente, usa `urllib` e
`struct`). Sem dependência externa.

```bash
git clone https://github.com/lucasferrazseo/og-image-check.git
cd og-image-check
```

## Como usar, passo a passo

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
Não nesta versão — cobre PNG, JPEG, GIF e WEBP, que são os formatos mais
comuns em `og:image` hoje.

**A ferramenta baixa a página inteira?**
Baixa o HTML da página (para achar a tag) e depois a imagem em si, para
ler as dimensões reais do arquivo.

## Limitações

Sem execução de JavaScript — se a tag `og:image` é montada via JavaScript
no navegador, este script não vê (o mesmo limite de leitura que a maioria
dos crawlers de compartilhamento também tem). Cobre PNG, JPEG, GIF e WEBP;
AVIF não tem parsing de dimensão implementado aqui.

## Autor

[Lucas Ferraz](https://lucasferraz.com) — especialista em SEO, criação de
sites e SEO para IA, fundador da [Lucas Ferraz SEO](https://lucasferrazseo.com).

## Licença

MIT — ver [LICENSE](LICENSE).
