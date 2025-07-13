# LangchainRAGTest

本專案是一個簡易的 RAG（Retrieval-Augmented Generation）系統，使用 LangChain、OpenAI Embeddings 與 Chroma VectorDB，將 PDF 文件轉為向量資料庫，並可根據使用者問題檢索相關內容並生成回答。

## 專案結構

```
.env
.gitignore
create_database.py         # 建立向量資料庫
query_data.py              # 查詢資料庫並生成回答
pyproject.toml
uv.lock
chroma/                    # Chroma VectorDB 資料夾
    chroma.sqlite3         # Chroma 資料庫檔案
    ...
data/
    books/
        漫步华尔街的10条投资金律(vikingcabin.com).pdf
        customer_info.md
```

## 主要功能

- 讀取 `data/books` 目錄下的 PDF 檔案，將內容分割並轉為向量，儲存於 `chroma` 資料夾。
- 使用 OpenAI Embeddings 進行文本向量化。
- 透過 `query_data.py` 輸入問題，檢索最相關的內容並用 OpenAI GPT 生成回答。

## 安裝與設定

1. 安裝 Python 相關套件（建議使用 virtualenv）：
    ```sh
    uv sync
    ```
    或根據 `pyproject.toml` 安裝。

2. 設定 `.env` 檔案，需包含 OpenAI API 金鑰：
    ```
    OPENAI_API_KEY=你的API金鑰
    ```

## 使用方式

### 1. 建立向量資料庫

執行以下指令，將 PDF 轉為向量並儲存至 Chroma DB：

```sh
python create_database.py
```

### 2. 問答查詢

執行查詢腳本，輸入你的問題：

```sh
python query_data.py
```

依照提示輸入問題，系統會回傳根據資料庫檢索與生成的答案。

## 相關檔案說明

- [`create_database.py`](create_database.py)：負責載入 PDF、分割文本、向量化並儲存至 Chroma。
- [`query_data.py`](query_data.py)：負責讀取 Chroma DB，根據輸入問題檢索並生成回答。
- [`data/books/`](data/books/)：放置欲處理的 PDF 文件與其他資料。
- [`chroma/`](chroma/)：Chroma VectorDB 資料與檔案。

## 注意事項

- 需有 OpenAI API 金鑰。
- PDF 檔案需放在 `data/books` 目錄下。
- 若要重新建立資料庫，會清除舊有的 `chroma` 資料夾。

---

本專案僅供學術與測試用途。
