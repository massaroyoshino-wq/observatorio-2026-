# Observatório 2026 — Empresas, eventos e declarações

Aplicativo web instalável (PWA), com busca por **empresa/estabelecimento/empresário**, filtros de segmento, UF e natureza da evidência, fontes clicáveis, exportação CSV, notícias e referências públicas indexadas de **Instagram, Facebook e X** pesquisadas diariamente.

## Abrir agora

Abra `index.html` no computador ou celular. O catálogo inicial funciona sem internet; o filtro inicial mostra apoios declarados (da marca ou da pessoa vinculada), não meras presenças em reuniões. O botão Atualizar só obtém novos dados quando hospedado.

## Publicar e instalar no Android (Galaxy)

1. Crie um **novo repositório GitHub**, separado de outros projetos, por exemplo `observatorio-2026`, e copie **todo o conteúdo desta pasta** para a raiz do repositório (incluindo a pasta `.github`).
2. Em **Settings > Pages**, em **Build and deployment > Source**, selecione **GitHub Actions**. O fluxo `Atualizar e publicar Observatório 2026` faz o deploy do site na branch `main` e a atualização diária dos feeds. Aguarde o endereço do GitHub Pages ficar acessível.
3. No smartphone, abra o endereço `https://SEU-USUARIO.github.io/observatorio-2026/` no Chrome. Toque no menu `⋮` > **Adicionar à tela inicial** / **Instalar app**.
4. A rotina `Atualizar e publicar Observatório 2026` é executada via **GitHub Actions todos os dias às 11:00 UTC = 08:00 em São Paulo**. É necessário habilitar GitHub Actions e permitir gravação por Actions quando as configurações do repositório exigirem. Os feeds novos são publicados no mesmo fluxo, sem depender de um novo disparo da branch.
5. Para testar a primeira coleta, acesse **Actions > Atualizar e publicar Observatório 2026 > Run workflow**. Veja os registros de execução. O cadastro confirmado não é modificado automaticamente; somente os feeds em análise são atualizados.

## Como funciona a atualização

* **data/registry.json**: base curada, alimentada apenas por provas documentais, com data, fonte e classificação. Não é modificada automaticamente; qualquer inclusão requer revisão humana.
* **data/news.json**: coletado automaticamente via Google News RSS a cada dia pelo script `scripts/update_news.py` (sem chave de API). As notícias aparecem na aba **Notícias em análise** e **não** alteram a classificação de empresas.
* **data/social.json**: links públicos do Instagram, Facebook e X que um buscador possa ter indexado, coletados pelo script `scripts/update_social.py` via resultados RSS. São **pistas sem validação de autoria, data da postagem ou apoio**; a aba **Instagram, Facebook e X** permite filtrar a plataforma e abrir pesquisas externas.
* **Filtro Origem da fonte**: separa imprensa/sites, Instagram, Facebook e X entre as evidências **curadas** do cadastro. O cadastro inicial não recebe automaticamente entradas novas de redes sociais.
* **Listas públicas não verificadas**: só reportagens que descrevem a circulação da lista, **sem copiar nomes de comerciantes não confirmados**.
* **Modo offline**: o aplicativo usa uma cópia embutida no HTML e service worker para elementos estáticos. Os dados mais recentes exigem conexão com a hospedagem.
* Se a coleta falhar, os dados antigos permanecem e a rotina registra a falha. Não há promessa de disponibilidade de feeds externos.

## Inclusão de estabelecimentos com evidências

Adicione uma entrada em `data/registry.json` com `name`, `sector`, `state`, `person` (se houver) e `evidence` com `type`, `date`, `summary`, `sourceName`, `sourceUrl` e `scope`. Para posts públicos, `sourceUrl` deve ser o link **direto e verificável da postagem original** (não link de busca). Instagram, Facebook e X aparecem automaticamente no filtro de origem a partir desse link.

Tipos aceitos:
- `apoio_estabelecimento`: manifestação pública feita pelo estabelecimento/marca;
- `apoio_individual`: declaração pública da pessoa vinculada a empresa, sem atribuir apoio institucional;
- `evento`: encontro confirmado, que não prova apoio eleitoral.

O HTML contém dados iniciais embutidos para funcionar aberto como arquivo local. Para distribuir uma nova versão offline, atualize também o JSON embutido no elemento `<script id="seed">` do `index.html`; quando hospedado, o `data/registry.json` é lido ao abrir e ao clicar em Atualizar.

## Avisos de interpretação

A participação em reunião institucional/econômica com o presidente não configura apoio eleitoral; verifique a matéria original. O voto é secreto; nunca deduza o voto de pessoas com base em listas ou em vínculo empresarial. O observatório é uma organização documental de registros públicos, sem vínculo com partido ou campanha.

## Instagram, Facebook e X: escopo real da coleta

* Esta versão monitora referências **públicas indexadas em buscadores** e oferece busca por assunto nas plataformas; não acessa contas privadas nem usa login do usuário. Uma publicação nova pode não estar indexada e, portanto, não ser capturada.
* Instagram e Facebook restringem a leitura automatizada de conteúdo pela API Meta, exigindo aplicativo, token, permissões e, em alguns casos, análise prévia para consultar contas que não são suas. O X oferece pesquisa de posts pela API, mas o acesso exige conta de desenvolvedor e token e pode ter custo. Nenhuma integração autenticada está configurada neste ZIP.
* Nunca trate curtidas, follows, repostagens, menções de terceiros, fotos de encontros ou presença em reunião como apoio eleitoral do estabelecimento. Cada entrada confirmada precisa de evidência explícita em fonte original e revisão humana.
* Nenhuma credencial deve ser colocada diretamente no HTML, no JSON público ou em repositório aberto. Se integrar APIs, use GitHub Secrets e um script de servidor ou Actions.
* A coleta social poderá retornar **zero** resultados, sem que isso signifique ausência de manifestações na rede. O arquivo `data/social.json` registra a última tentativa.

## Limitações

Esta entrega é uma PWA e **não é um APK nativo**. Uma PWA precisa de HTTPS para ser instalada em navegadores compatíveis. O ZIP inclui um site pronto para publicação, mas o conteúdo **não está publicado no GitHub** e a atualização diária **só começa quando o projeto for hospedado e o GitHub Actions for habilitado**. Não confundir notícias automáticas com novas adesões confirmadas.

## Revisão da versão 1.2

* Excluído da classificação de apoio o **Instituto da Patroa**: a reportagem disponível fala de uma lista de boicote e de ofensas, mas não documenta declaração explícita de apoio à candidatura. A reportagem permanece na seção de listas como contexto, sem nomes acusatórios.
* A fonte da **Risotropical / Publica** é um espelho de uma postagem do Instagram. Por isso sua origem é marcada como Instagram, com a ressalva de que o original não foi acessível diretamente.
* A página inicia na visualização de **apoios declarados**, deixando a presença em eventos como filtro distinto; isso evita classificar a participação em reuniões econômicas como endosso eleitoral.
* A publicação automática **não** revisa nem adiciona apoios ao cadastro; somente atualiza feeds de notícias e de URLs sociais em análise.
* Para publicar é preciso criar um repositório novo, pois o repositório do Dividendos Auto deve permanecer independente.