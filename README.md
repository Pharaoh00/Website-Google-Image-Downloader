# Website-Google-Image-Downloader
## Um simples script para download imagens de websites e google image.

Requer **requests**
Requer **BeautifoulSoup**

###### Para instalar requests
```
pip install requests
```

###### Para instalar BeautifoulSoup
```
pip install beautifulsoup4
```

Os comentarios estão em em Português Brasil, em algum momento, quando eu estiver feliz com os resultados do script, estarei traduzindo os comentarios para Inglês.

Como utilizar(Na versão atual V0.3):
em url = "https://www.google.com/search?..." copie e cole a url desejada.
Parse_Image() aceita dois modos:
```
    mode = NORMAL ou GOOGLE
    NORMAL significa que o site desejado não é o google, qualquer outro site.
    (PS: As imagens podem ser procurada por simples "img" / "src")
    Google significa que o site desajado é o google imagens.
    (PS: As imagens são procurada por "div" "class: rg_meta notranslate",
    essa classe contem todas as informações do site da imagem, inclusive a url,
    a classe é na verdade um json, dentro do json gerado a url da imagem esta 
    em ["ou"].
```
Logging será a forma principal de output o que foi baixado, qual a url da image, e qual o nome do arquivo salvo.
Acredito que eu não tenha descoberto todos os erros possíveis, mas os erros que já foram dados estão, pelo menos, output para o arquivo de log.
