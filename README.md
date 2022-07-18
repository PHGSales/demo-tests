# Instruções

A ideia desse repositório é exemplificar um modelo de desenvolvimento com testes. Em linhas gerais, a ideia 
é ter testes para todos os métodos da aplicação, garantindo que que ela funciona e, caso haja alguma alteração no 
código, os testes serão um farol para entender quais os efeitos da alteração sobre o funcionamento da aplicação (quais 
métodos tiveram seu comportamento alterado).

## Instruções sobre como usar o repositório:
Para iniciar o repositório, basta executar o comando `make dev-setup` na raiz so repositório. Se der algum erro, 
verifique se a sua variável de ambiente `PYTHONPATH` está correspondendo ao caminho da sua raiz do projeto.

Para executar os testes, após estar com o ambiente virtual ativado, basta executar o comando `make test`.

## Organização das pastas:
O repositório está dividido em duas metades: src e test, onde a pasta de src corresponde à aplicação em si e a parta se 
test à replicação da estrutura da aplicação, mas contém somente testes.<br>
Os arquivos de teste replicam a estrutura dos arquivos da aplicação, porém, com arquivos nomeados 
`test_{nome do arquivo testado}`.

## Organização dos testes:
Os testes estão divididos da seguinte maneira: uma classe de teste nomeada `Test{nome da clsse testada}` e os métodos 
das classes de teste sempre começam com `test_` para que o pytest possa reconhecer como um teste.