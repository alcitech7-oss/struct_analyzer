```markdown
# 🏗️ Struct Analyzer

Uma ferramenta inteligente que analisa a estrutura de qualquer site, extraindo **todas as tags, classes, IDs, links e textos**, e organiza tudo em uma planilha Excel com **seletores CSS e XPath prontos para uso**.

> 💡 **Ideal para:** Automação web, raspagem de dados, testes automatizados, e análise de estrutura de sites sem precisar ficar caçando no F12!

---

## 🎯 Para que serve?

- **Mapear a estrutura completa** de qualquer site
- **Extrair seletores CSS e XPath** automaticamente
- **Entender a hierarquia** do DOM com profundidade e posição
- **Usar com I.A.** — cole a planilha e peça seletores específicos
- **Economizar horas** de inspeção manual no navegador

---

## 📋 O que a planilha te entrega

| Coluna | O que é | Exemplo |
|--------|---------|---------|
| **posicao** | Ordem do elemento na página | `13` |
| **profundidade** | Nível no DOM (0 = raiz) | `3` |
| **tag** | Nome da tag HTML | `h1`, `div`, `a` |
| **classe** | Classes CSS | `title`, `header`, `btn-primary` |
| **id** | ID do elemento | `#error-code`, `#app` |
| **seletor_css** | 🔥 Seletor CSS pronto | `.title`, `#error-code` |
| **xpath** | 🔥 XPath pronto | `//h1[contains(@class, "title")]` |
| **link** | URL (se for um link) | `https://...` |
| **texto** | Conteúdo textual | `"Não é possível acessar"` |
| **pai** | Tag do elemento pai | `main`, `body` |

---

## 🚀 Como usar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/struct-analyzer.git
cd struct-analyzer
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
playwright install
```

### 3. Rode o script
```bash
python main.py
```

### 4. Digite a URL
```
🌐 Qual site você quer analisar? https://www.uol.com.br/
```

### 5. Pronto!
O arquivo `estrutura_20260701_143022.xlsx` será gerado com toda a estrutura do site.

---

## 💬 Como usar com I.A. (ChatGPT, Claude, etc.)

**1. Rode o Struct Analyzer** no site que você quer analisar

**2. Cole a planilha na conversa com a I.A.**

**3. Faça perguntas como:**
> - "Me dá o seletor do menu de navegação"
> - "Qual a classe dos títulos das notícias?"
> - "Como eu pego todos os links da barra preta?"
> - "Qual o XPath do botão de login?"

**4. A I.A. olha a planilha e te dá os seletores prontos!**

```python
# Exemplo: a I.A. te responde com o seletor
seletor = ".headerDesktop__menu"
elementos = page.query_selector_all(seletor)
```

---

## 📊 Exemplo de saída

| posicao | profundidade | tag | classe | id | seletor_css | texto |
|---------|--------------|-----|--------|----|-------------|-------|
| 9 | 2 | header | header | | .header | |
| 13 | 3 | h1 | title | | .title | Não é possível acessar |
| 20 | 3 | a | btn | | .btn | Falar com o Magalu |

---

## 🛠️ Tecnologias

| Tecnologia | Função |
|------------|--------|
| **Python** | Linguagem principal |
| **Playwright** | Navegação e extração de elementos |
| **Pandas** | Manipulação de dados |
| **OpenPyXL** | Geração de planilhas Excel |

---

## 📦 Dependências

```txt
playwright==1.40.0
pandas==2.1.0
openpyxl==3.1.0
```

---

## 🔧 Personalização

Quer mudar algo? O código é modular:

- `analisar_estrutura(url)` → Extrai os dados do site
- `gerar_seletor_css(tag, classe, id)` → Gera seletores CSS
- `gerar_xpath(tag, classe, id, posicao)` → Gera XPath
- `salvar_excel(dados)` → Salva a planilha

---

## ⚠️ Limitações

- Sites com **bloqueio de bot** (ex: Cloudflare) podem retornar erro 403
- Conteúdo **carregado via JavaScript** é capturado (Playwright é headless)
- Textos muito longos são limitados a 300 caracteres

---

## 📝 Licença

MIT - Use à vontade! 🚀

---

## 🤝 Contribuindo

Quer melhorar? Manda um PR ou abre uma issue!

---

Feito com ❤️ para quem cansou de ficar caçando no F12.
```