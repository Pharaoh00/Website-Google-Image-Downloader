# Website-Google-Image-Downloader
## Um simples script para download imagens de websites e google image.

Requer **requests**

Requer **BeautifulSoup**

###### Para instalar requests
```
pip install requests
```

###### Para instalar BeautifulSoup
```
pip install beautifulsoup4
```

Os comentarios estão em em Português Brasil, em algum momento, quando eu estiver feliz com os resultados do script, estarei traduzindo os comentarios para Inglês.

Como utilizar(Na versão atual v1.0):

Em main.py
Em url = "" 
Adicione a url desejada.

Em home = ""
Adicione a homepage do website.

A versão atual utilizada somente requests para conseguir baixar as imagens. Muitos sites utilizam-se se js scripts para autenticar o usuário, por isso sites como CNN, Globo.com, Wikipedia, Terraria Wiki acabam não deixando a imagem ser baixar com esse script.
Felizmente há alguns métodos, como Selenium, para conseguir baixar em sites como esses, mas nesse momento, essa ferramenta em questão, será usada para baixar imagens do google image, e em alguns outros sites (por sorte consigo baixar em todos que preciso).

Há se fazer:
Adicionar Selenium como força de download. Adicionando versatilidade ao script.
Adicionar async nos requests para pegar as urls das imagens.
Adicionar uma forma eficaz de output o que aconteceu no download.
(PS: Pretendo usar um json, como agora é uma classe, posso estar append todas as urls em algum formato e criando um json para informar)
Adicionar barra de progresso, em vez de mensagens sem sentido rolando na tela.
