
# XML Converter

_XML Converter_, ou simplesmente _XC_, é uma das ferramentas que fazem parte do _SciELO PC Programs_, para **usuários gestores de coleção SciELO**.

Sua principal função é a geração de bases de dados _ISIS_ nas pastas que seguem o padrão: `serial/<acron>/<volnum>/base/<volnum>` para uso do _GeraPadrao_ e também organizar os arquivos do pacote na estrutura do sítio web de _Controle de Qualidade_ nas pastas `xml`, `pdf`, `img/revistas`.

_XML Converter_ executa as mesmas validações feitas pelo _XML Package Maker_, mas também valida os dados dos pacotes contra os dados registrados nas bases _title_ e _issue_. Somente se os pacotes forem válidos, sua base de dados correspondente será criada.

A partir da versão 4.0.097, pode-se configurar a disponibilização dos pacotes para a nova plataforma de publicação _SciELO Publishing Framework_, mais especificamente para consumo do _KERNEL_.


# XML Converter for server

Na versão _XML Converter for server_, pode-se configurar opcionalmente para:

 - baixar, de um outro servidor via _FTP_, os pacotes compactados de documentos SciELO (https://scielo.readthedocs.io/projects/scielo-publishing-schema/pt_BR/latest/).
 - acionar a execução do _GeraPadrao_ do sítio web de _Controle de Qualidade_.
 - disponibilizar (publicar) os arquivos de bases, pdf, imagens, xml etc em um servidor remoto, caso o sítio web de _Controle de Qualidade_ não rode no mesmo servidor em que é executado o _GeraPadrao_ do sítio web de controle de qualidade. 


## Pré-requisitos

 - Linux
 - CISIS
 - Python 3.x
 - SciELO Packtools


## Instalação

Criar a seguinte estrutura de pasta: 

 - `<raíz>`
   - `xml` (pasta com os programas)
   - `config` (arquivos de configurações)

Os nomes `xml` e `config` são fixos.
O diretório `<raíz>` se refere à versão do _XC_, por exemplo, `xc_2020`.

**Nota:** Uma mesma instalação (instância) pode servir para mais de uma coleção.
Não é necessária criar diferentes instâncias para cada coleção. Basta criar um arquivo de configuração para cada coleção.

## Configuração

O arquivo de configuração deve ficar em `<raíz>/config`.
O seu nome deve ser seguir o seguinte padrão: `<collection_acron>.xc.ini`.


### Configurações obrigatórias

Indique o **caminho dos utilitários CISIS**, ou seja, a pasta cisis que contém os utilitários CISIS que são usados no _GeraPadrao_. No caso, da versão _XC server_ usar o mesmo caminho para ambas variáveis.

Exemplo:

```
PATH_CISIS_1030=/bases/xml.000/proc/cisis
PATH_CISIS_1660=/bases/xml.000/proc/cisis
```

Indique respectivamente as **bases de dados _ISIS_ de _issue_ e _title_ que são enviadas continuamente** pelo utilitário _EnviaBasesXML.bat_ instalado no servidor local Windows. Estas bases serão copiadas todas as vezes que iniciar um processo do _XC_.

Exemplo:

```
SOURCE_ISSUE_DB=/bases/xml.000/serial_proc/issue/issue
SOURCE_TITLE_DB=/bases/xml.000/serial_proc/title/title
```

Indique respectivamente as **cópias** bases de dados _ISIS_ de _issue_ e _title_ que são enviadas pelo utilitário _EnviaBasesXML.bat_ instalado no servidor local Windows. Estas bases serão criadas e indexadas todas as vezes que iniciar um processo do _XC_.

Exemplo:

```
ISSUE_DB_COPY=/bases/xml.000/collections/scl/xmldata/issue/issue
TITLE_DB_COPY=/bases/xml.000/collections/scl/xmldata/title/title
```

Indique onde está instalado a estrutura da aplicação _Web_ (sítio web da metodologia Clássica) onde correrá _GeraPadrao_ para o sítio web de _Controle de Qualidade_.

**Nota**: Caso exista mais de uma instância de _XC_ executando concorrentemente, pode-se compartilhar a mesma instância

Exemplo:

```
LOCAL_WEB_APP_PATH=/bases/xml.000/collections/scl/scl.000
```

Indique onde está instalado a **estrutura da pasta _serial_** que tem duas funções principais: armazenamento das bases de dados para o _GeraPadrao_ do sítio web de _Controle de Qualidade_ e também para que a cada entrada de pacotes o _XC_ possa validar os novos pacotes com os dados anteriormente registrados.

**Nota**: Caso exista mais de uma instância de _XC_ executando concorrentemente, pode-se compartilhar a mesma instância

Exemplo:

```
PROC_SERIAL_PATH=/bases/xml.000/collections/scl/scl.000/serial
```

Indique os caminhos dos diretórios usados pelo _XC_ como **área de trabalho**.

Pasta para criar arquivos temporários

```
TEMP_PATH=
```

Pasta para as filas dos pacotes a serem processados pelo _XC_.

```
QUEUE_PATH=
```

Pasta para receber os pacotes via FTP ou mesmo manualmente. O _XC_ lê esta pasta e **move** para `QUEUE_PATH`.

```
DOWNLOAD_PATH=
```

Pasta para arquivar os pacotes, caso seja desejável mantê-los, caso contrário, deixar em branco. Mas pode ocupar espaço considerável.

```
ARCHIVE_PATH=
```

### Configurações Desejáveis

O _XC_ no servidor se comunica com o usuário pelas mensagens na tela mas também por email.
Funciona sem esta configuração, no entanto, a comunicação fica um pouco comprometida.

Indique se **a funcionalidade de envio de email**  deve ou não ocorrer. Valores possíveis: **on** ou **off**

Exemplo:

```
EMAIL_SERVICE_STATUS=
```

Indique os dados do **remetente** das mensagens.

```
SENDER_NAME=
SENDER_EMAIL=
```

Indique o endereço de email ou endereços separados por ';' dos **usuários do _XC_**.

```
EMAIL_TO=
```

Indique o endereço de email para receber **mensagens de exceções**.

```
EMAIL_TO_ADM=
```

Configure o **assunto** e **conteúdo** de cada tipo de mensagem.
Troque `COLLECTION_NAME` pelo nome da coleção.
Troque `XC_VERSION` pela identificação da instância (número ou ano da versão) de _XC_.
Os arquivos `*.txt` ficam em `<raíz>/xml/prodtools/settings/email/`.

**Nota:** Alterar o conteúdo destes arquivos pode impactar nas mensagens do _XC_ para outras coleções.
Para criar mensagens personalizadas, crie novos arquivos.

```
EMAIL_SUBJECT_PACKAGE_EVALUATION=[XC_VERSION] [COLLECTION_NAME] Evaluation report of  
EMAIL_TEXT_PACKAGE_EVALUATION=email.txt

EMAIL_SUBJECT_PACKAGES_RECEIPT=[XC_VERSION] [COLLECTION_NAME] Packages receipt report
EMAIL_TEXT_PACKAGES_RECEIPT=email_download.txt

EMAIL_SUBJECT_GERAPADRAO=[XC_VERSION] [COLLECTION_NAME] homolog.xml.scielo.br is updated
EMAIL_TEXT_GERAPADRAO=email_gerapadrao.txt

EMAIL_SUBJECT_INVALID_PACKAGES=[XC_VERSION] [COLLECTION_NAME] Invalid packages
EMAIL_TEXT_INVALID_PACKAGES=email_invalid_packages.txt
```

### Configurações Opcionais

Preencher somente se as operações opcionais serão executadas


#### Recepção de pacotes por FTP

Preencher somente o _XC_ baixará os pacotes por FTP.

Indique os dados do **local de onde os pacotes serão baixados**.

```
FTP_SERVER=
FTP_USER=
FTP_PASSWORD=
FTP_DIR=
```

#### Execução do GeraPadrao

Caso seja desejável que o _XC_ acione a execução do _GeraPadrao_, todas as variáveis abaixo devem ser configuradas.
**Nota**: Caso exista mais de uma instância de _XC_ executando concorrentemente, **escolher apenas 1** delas para acionar a execução do _GeraPadrao_


Indique onde está instalado **proc** do _GeraPadrao_.

Exemplo:

```
PROC_PATH=/bases/xml.000/collections/scl/scl.000/proc
```

Indique **o caminho do arquivo temporário scilista** que contém ítens processados com sucesso pelo _XC_. Neste arquivo ficam acumulados todos os ítens validados pelo _XC_ até que o _GeraPadrao_ o consuma.

Exemplo:

```
COL_SCILISTA=/bases/xml.000/collections/scl/xmldata/minha_scilista.txt
```

Indique **o caminho do arquivo que controla a execução do _GeraPadrao_** que contém os valores **FINISHED** ou **running**. Serve como um "semáforo" impedindo que mais de um processo de _GeraPadrao_ rode concorrentemente para a mesma coleção.

Exemplo:

```
GERAPADRAO_PERMISSION=/bases/xml.000/collections/scl/xmldata/gerapadrao.controle.txt
```

#### Publicação do sítio web de controle de qualidade

Preencher somente se o resultado será visualizado em um sítio web de controle de qualidade

Exemplo:

```
WEB_APP_SITE=homolog.xml.scielo.br
```

#### Disponibilização de arquivos para o sítio web de controle de qualidade se é remoto

Preencher somente se o sítio web de controle de qualidade é remoto.

Indique **a transferência deve ou não ocorrer**. Valores possíveis: **on** ou **off**

Exemplo:

```
TRANSFERENCE_STATUS=
```

Indique os dados do **destino do sítio web de controle de qualidade**.

```
TRANSFER_USER=
TRANSFER_SERVER=
REMOTE_WEB_APP_PATH=
```

#### Disponibilização de pacotes para o Kernel

**Por FTP**

Preencher apenas o necessário para executar a transferência. Dependendo da infraestrutura, pode ser o suficiente apenas o endereço do servidor remoto e o caminho do destino.

```
KG_server=
KG_user=
KG_password=
KG_remote_path=
```

**Por cópia**

```
KG_destination_path=
```

## Execução

Combinações possíveis de comandos:

Para executar a função principal do _XC_, ou seja, a geração de dados para o sítio web clássico.

`cd <raíz>/xml;xc_server <collection_acron>`


Para executar primeiro o download dos pacotes e depois a geração de dados para o sítio web clássico.

`cd <raíz>/xml;xc_server <collection_acron> [--download]`


Para executar primeiro o download dos pacotes, a geração de dados para o sítio web clássico e, por fim, aciona a execução do _GeraPadrao_ do sítio web de controle de qualidade.

`cd <raíz>/xml;xc_server <collection_acron> [--download] [--gerapadrao]`


Para executar a geração de dados para o sítio web clássico e, por fim, aciona a execução do _GeraPadrao_ do sítio web de controle de qualidade.

`cd <raíz>/xml;xc_server <collection_acron> [--gerapadrao]`


Pode-se deixar agendado a execução dos comandos conforme a necessidade.
Por exemplo, colocar com mais frequência:

`cd <raíz>/xml;xc_server <collection_acron> [--download]`

e menor frequência:

`cd <raíz>/xml;xc_server <collection_acron> [--download] [--gerapadrao]`


Pode-se deixar agendado a execução de _XC_ a cada 5 minutos, dentro de um período, por exemplo, de 7h às 19h.
No entanto, o horário não deve coincidir com outras versões de _XC_ que podem rodar concorrentemente.
O motivo é que todas as instâncias de _XC_ fazem modificações na mesma pasta `serial`.

Caso exista **mais de uma** instância de _XC_ executando concorrentemente, **escolher apenas 1** delas para acionar a execução do _GeraPadrao_.

