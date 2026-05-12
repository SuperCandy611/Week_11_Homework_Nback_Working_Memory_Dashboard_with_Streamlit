# Week 11 Homework — N-back Dashboard (Starter)

> 把這份資料夾複製到自己的 GitHub repo，把 `TODO` 區塊填完整即可。

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

App 開在 <http://localhost:8501>。

## Files

```
.
├── app.py                          ← 你要改的檔案（含 5 個 TODO）
├── data/
│   └── nback_working_memory.csv    ← 不要改動
├── requirements.txt
└── README.md                        ← 改成你自己的 README
```

## What to do

完整作業說明見 `week-11-homework.md`（在 homeworks/week11 根目錄）。
最低要求：完成 TODO 1–5 + 部署到 Streamlit Cloud。

## Submission

繳交：

1. GitHub repo URL（public）
2. Streamlit Cloud URL
3. 一張 dashboard 截圖

## How to Run

### 前置條件

- Python 3.9 以上
- `data/nback_working_memory.csv` 必須存在（請勿修改）

### 1. 建立並啟動虛擬環境

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

### 2. 安裝套件

```bash
pip install -r requirements.txt
```

### 3. 啟動 Dashboard

```bash
streamlit run app.py
```

Streamlit 會顯示本機網址（預設為 <http://localhost:8501>），在瀏覽器開啟即可。

### 4. 操作說明

| 區域 | 說明 |
|------|------|
| **Sidebar** | 可依年齡範圍、性別（`F`/`M`）與 N-back 條件（`1-back` / `2-back` / `3-back`）篩選資料 |
| **Metric tiles** | 即時顯示篩選後的資料筆數、平均 accuracy 與平均 reaction time |
| **Overview tab** | 以散點圖呈現各 condition 的 accuracy 與 RT 隨年齡的分布 |
| **By Condition tab** | 條件別摘要表、accuracy 與 RT 長條圖，以及 d′ 敏感度折線圖 |
| **Raw Data tab** | 顯示篩選後的完整資料表，並提供 CSV 下載按鈕 |

> 若 app 顯示找不到 CSV 的錯誤，請確認 `data/nback_working_memory.csv` 與 `app.py` 位於同一層目錄下。

---

## Reflection

這個 dashboard 最適合**認知心理學或神經科學領域的研究者與研究生**。我期待這個族群應該會熟悉 N-back 典範與 d′ 指標，能直接從「By Condition」分頁的準確率與反應時間折線看出工作記憶負荷效應，也能透過 Overview 的散點圖快速辨識年齡與表現的相關趨勢。相比之下，一般大眾對 d′ 或 1-back/3-back 術語較陌生，需要更多說明才能解讀。若目標觀眾改為大眾，可能需要加入更多白話說明與情境化敘述。
