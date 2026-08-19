# Logica de Precificacao

Esta pasta concentra a base que a calculadora deve consultar. Os catalogos originais e os arquivos convertidos continuam em `../referencias` e `../catalogos-md` como fonte de auditoria.

## Arquivos

- `catalogo-midias.xlsx`: base editavel para operacao comercial.
- `../catalogos-md/catalogo-midias.xml`: fonte estruturada usada para gerar a planilha.
- `../catalogos-md/gerar_catalogo_xlsx.py`: gerador da planilha a partir do XML.

## Como a calculadora usa a base

1. Filtra a aba `Midias` por `Tipo`, `Cidade` e `Ativa = true`.
2. Exibe apenas as midias com `Disponibilidade = disponivel` ou sem status de indisponibilidade.
3. Busca na aba `Precos` todas as linhas com o mesmo `Midia ID` da midia selecionada.
4. Multiplica ou soma o valor conforme a unidade do preco, como `mes`, `bi-semana`, `carro-mes`, `face-mes` ou `unidade`.
5. Permite acrescentar itens da categoria `adicional`, como producao de VT, producao de lona ou instalacao.
6. Para outdoors com varios locais, mostra os registros da aba `Pontos` para o usuario selecionar os pontos desejados.
7. Mostra as regras aplicaveis da aba `Condicoes` no resumo da proposta.

## Atualizacao comercial

1. Inclua ou altere a midia e seus valores no arquivo XML.
2. Mantenha o arquivo de origem cadastrado em `Fontes` para rastreabilidade.
3. Use `ativo="false"` e `disponibilidade="indisponivel"` para guardar uma midia sem oferecela na calculadora.
4. Execute `python ../catalogos-md/gerar_catalogo_xlsx.py` a partir desta pasta, ou execute o script pelo caminho completo, para atualizar a planilha.
