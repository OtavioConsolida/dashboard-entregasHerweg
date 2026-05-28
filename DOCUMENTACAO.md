# Documentação do Dashboard de Entregas (Consolida / Herweg)

Este documento centraliza todas as regras de negócio, a arquitetura do painel e as instruções de uso. Ele deve ser consultado e **atualizado obrigatoriamente** sempre que houver mudanças estruturais no projeto.

---

## 1. Visão Geral e Arquitetura
O Dashboard de Entregas é uma aplicação web "client-side" (Front-end) desenvolvida para processar planilhas brutas de entregas logísticas, classificar automaticamente a performance das transportadoras e apresentar gráficos de leitura executiva.

**Tecnologias Utilizadas:**
* **Core:** HTML5, CSS3, JavaScript (Vanilla).
* **Bibliotecas Externas:** 
  * `Chart.js` (para renderização dos gráficos).
  * `SheetJS / xlsx` (para leitura e exportação do arquivo Excel no próprio navegador, sem necessidade de backend).
* **Autenticação:** Firebase Auth (proteção da tela principal e funções exclusivas de Admin).
* **Hospedagem:** GitHub Pages.

---

## 2. Como Usar (Fluxo do Usuário)
1. **Login:** Acessar a URL do GitHub Pages e inserir as credenciais cadastradas no Firebase.
2. **Carregamento de Dados:** Na tela inicial, o usuário clica na área de upload e seleciona o arquivo Excel exportado pelo seu sistema ERP (ex: `registros.xlsx`).
3. **Filtros:** Após o carregamento, o sistema habilita filtros por mês, UF e Status originais. Os gráficos e tabelas reagem instantaneamente a essas seleções.
4. **Análise:** O painel se divide em Gráfico SLA (Geral), Gargalos por Cidade (Top 10 piores rotas), Performance por Transportadora e o Ranking Geral detalhado.
5. **Central de E-mails:** O usuário pode alternar para a aba de e-mails, selecionar uma transportadora, escolher os tipos de falha que deseja cobrar e gerar um código HTML. Um botão copiará esse visual para ser colado (Ctrl+V) no Outlook.
6. **Exportação:** É possível baixar a planilha novamente contendo a visão atualizada e filtrada.

---

## 3. Origem e Tratamento dos Dados
O painel não possui um banco de dados próprio para armazenar as notas. Os dados residem **exclusivamente na planilha** que o usuário sobe no momento do uso (arquitetura *stateless* e segura).

**Colunas Chaves Mapeadas pelo Sistema (case-insensitive):**
O script inteligente varre a planilha buscando as colunas que contenham termos específicos:
* **Nota:** `nf-e` ou `nota`
* **CT-e:** `ct-e`, `doc.frete` ou `frete`
* **Remetente:** `remetente`
* **Destino:** `destino` ou `cidade`
* **Prazos e Datas:** `prazo entrega` e `data entrega`
* **Status Original:** `situa` ou `status`

---

## 4. Regras de Negócio: Os 5 Status Logísticos
O coração do Dashboard é a função `resolveStatusLogico`. Como o ERP de origem muitas vezes exporta status confusos como *"Sem informação"*, *"Sem previsão"* ou *"Em andamento"*, o painel os **recalcula** com base no relógio (data atual vs prazos) transformando a base de dados em **5 status absolutos**:

1. **No prazo:**
   - *Se em trânsito:* A data limite (Prazo) é igual a hoje ou está no futuro.
   - *Se entregue:* A data de entrega ocorreu antes ou exatamente no dia do Prazo.
2. **Em atraso:**
   - Ainda não foi entregue e a data do Prazo já ficou no passado (ontem para trás).
3. **Entregue em atraso:**
   - Já tem Data de Entrega preenchida, porém ocorreu em uma data posterior ao Prazo.
4. **Sem prazo:**
   - Ainda não foi entregue e a coluna "Prazo de Entrega" está VAZIA.
5. **Entregue sem prazo:**
   - Já possui Data de Entrega, mas a nota nunca teve um Prazo registrado no sistema.

**Impacto na Exportação de Dados:**
Quando o usuário clica em **Exportar Visão**, o painel recria a planilha original com 100% de fidelidade (mesmas colunas, mesma ordem). A única alteração feita pelo robô é **sobrescrever** a coluna de "Situação" velha pelo novo status calculado (um dos 5 descritos acima).

---

## 5. Regras Visuais e Gráficos

* **Gráfico SLA (Rosca):** Exibe o total geral agrupando em fatias.
* **Gargalos por Cidade (Barras Horizontais):** Mostra **apenas o TOP 10** das piores cidades. A régua de pioridade é a soma dos problemas: `(Em Atraso + Entregue em Atraso + Sem Prazo + Entregue Sem Prazo)`.
* **Performance por Transportadora (Barras Empilhadas):** Mostra o Top 15 transportadoras.
* **Tabela de Ranking:** Exibe os números brutos por transportadora.
  - A coluna `% Atraso` soma estritamente os atrasos: `((Em Atraso + Entregue em Atraso) / Total Notas) * 100`.
  - Pílulas Coloridas: Acima de 15% de atraso = Vermelho (Crítico). Acima de 5% = Amarelo (Atenção).

---

## 6. Painel Exclusivo Admin
Se o e-mail logado for exatamente igual à constante `ADMIN_EMAIL` definida no código (ex: e-mail diretor), uma seção adicional aparece abaixo do Ranking de transportadoras.
Esta aba (Gargalos Sem Prazo) isola e agrupa todas as notas que caem na regra de falha de previsão (`Sem Prazo` e `Entregue Sem Prazo`) agrupando por **Transportadora + Destino + Situação**, facilitando a identificação da raiz de falhas de SLA provocadas por erro sistêmico de lançamento.

---

## 7. Manutenção
Para desenvolvedores operando neste repositório:
* Este arquivo (`DOCUMENTACAO.md`) é um documento vivo. 
* Se novas condições de SLA, novas colunas no relatório de cobrança, ou novos relatórios gerenciais forem inseridos em `script.js` ou `index.html`, este arquivo deve refletir a mudança no mesmo commit.
