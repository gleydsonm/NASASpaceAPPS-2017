Team Flash - Space APPS 2017

Impacto: O projeto inova na tratativa flexivel de sondas de origem e 
  aquisição de dados, utilizando para isso redes sociais, satelites e
  microcontroladores,sensores de dispositivos moveis(celulares/tablets)
  como tambem sensores LPWAN integrando varias bases de dados fornecendo uma
  visao unica para o usuario ao mesmo tempo que fornecendo para eles
  tecnicas de machine learning para analise e correlacao de dados.


O modelo do projeto permite que ele seja flexivel quanto ao crescimento e coletas
de dados. O projeto é distribuido sob licença GPL, atualmente dividimos as sondas
em 3 categorias:
   - Fora do planeta: Fornecidos por dispositivos, Ex: Satelites, naves espaciais, dados históricos, etc
   - Locais: Fornecidos por microconroladores: sondas para captacao de dados relativos a fenomenos climaticos locais
      (massa de tempestade, raios, trovoes, chuva, etc)
   - Sociais: Fornecidos por seres humanos, atraves da analise de padroes publicados
     em perfis, alem de correlacionar dados relacionados a localizacao do perfil.
    

Com isso o projeto visa balancear os pros e contras de tipos tradicionais de 
origem de dados criando um ponto de aceitacao tanto do ponto de vista mercadologico
e precisao na analise de dados. Cada tipo de sonda possui suas vantagens/desvantagens:

Sondas por dispositivos:
  Pros
    - Alta precisao dos dados gerados
    - Possibilidade de calibragem e adequacao dos sendores para atender finalidades
      especificas, aajuste de escala de funcionamento etc
  Contras
    - Requer cursos de equipamentos
    - Requer custos de manutencao
    - Altosr custos de transmissao


Sondas fornecidas por midias sociais:
  - Baixo custo de aquisicao de dados
  - Nao requer hardware
  - Permite coleta global de dados e analise de padroes
  - Baixo custo de manutencao
  
  Contras:
  - Possiveis falsos positivos, necessidade de amostra maior para reduzir percentual
  de erros


O projeto utiliza codigo fonte livre, licenciado sob a licenca GPL utilizando
as linguagens de programacao C e Python, (descrever outras aqui)

Ele permite o estudo e aprimoramento constante de seu codigo fonte utilizando
a estrutura de trabalho colatorativo fornecida pelo Github, onde qualquer um
pode fazer o fork do projeto, entender os mecanismos usados para desenvolvimento
da metodologia e enviar sugestões de mehorias e correções.

O fluxo de operação do projeto é descrito no arquivo FluxoProjeto.graphml

Todo o desenvolvimento inicial assim como os módulos concluidos foram ralizados durante 
o NASA Space APPS 2017, onde foram concluidos os seguintes módulos:

Coleta local:

- Sonda coletora de dados usando ESP8666-12, utilizando comunicacao de dados sem fio para
  a API coletora de dados
- Comunicacao usando SocketIO, garantindo alta velocidade na transmissao de eventos ocorridos
  nos microcontroladores
- Configuracao facilitada de microcontroladores com suporte total a WPS
- Operacao usando sondas reais e emuladas (em caso de falha nos sensores)
- Nivel de sinal WIFI tambem usado como sonda de coleta de dispositivo local

Coleta Social:
- Scan do perfil do twitter em busca de padroes relacionados a eventos climativos
- Sonda inteligente de analise, com suporte a deteccao de expressoes em Ingles e Portugues do Brasil
- Mecanismo de deteccao de tragedias naturais baseadas
- Deteccao do nivel de criticidade e priorizacao da mensagem de acordo com o nivel
  de padroes detectados (terremotos, tsunamis tem mais urgencia e preferencia do que
  chuva, sol)

Banco de dados Nao relacional
- Armazenamento de dados em formato apropriado para pesquisa utilizando formato NOSQL
- Orientado a colecoes de dados
- Pode armazenar dados de diferentes formas sem que uma estrutura padrao e infexivel seja definida no inicio do projeto, assim possibilitando o mais diversos tipos de dados vindo de fontes diferentes sem que a perfomance seja afetada ou qualquer mudanca ou manutencao seja necessaria para a insercao de novos campos ou tipo de dados.
