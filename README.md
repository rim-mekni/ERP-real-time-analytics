# Real Time Analytics and Stream Processing for Intelligent ERP Systems

Data Science Lab I project, Eötvös Loránd University (ELTE), Faculty of Informatics

Student: Rim Mekni
Supervisor: Georgina

## About the project

ERP systems usually analyse business data in batch mode (for example with daily reports), so problems are detected late.
In this project I study how stream processing can give near real time insights in an ERP context, and I compare it with classic batch analytics.

The KPI followed in the project is the **late delivery rate**.

## Dataset

I use the **DataCo Smart Supply Chain** dataset (180,519 order items, 2015 to 2018).

The dataset is not included in this repository because the file is too large.
Download it from Kaggle: https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis

Put `DataCoSupplyChainDataset.csv` in the same folder as the notebook before running the code.

## Files

| File | Description |
|---|---|
| `Exploratory data analysis.ipynb` | Data understanding, cleaning, exploratory data analysis and baseline 1 (batch daily report). It also creates `dataco_clean.csv`. |
| `Stream baselines.py` | Streaming simulation: the orders are replayed one by one in date order. Baseline 2 (fixed threshold) and baseline 3 (z score on past days only). |
| `Literature_Review.xlsx` | Spreadsheet with the 10 scientific papers (title, date, publisher, datasets, method, findings, limitations). |
| `fig_*.png` | Charts used in the report. |
| `Requirements.txt` | Python libraries needed. |

## How to run

1. Install the libraries:
```
pip install -r Requirements.txt
```
2. Run the notebook `Exploratory data analysis.ipynb` (this creates `dataco_clean.csv`).
3. Run the streaming script:
```
python "Stream baselines.py"
```

## First results

| Method | Alert days |
|---|---|
| Baseline 2: fixed threshold (65%) | 86 |
| Baseline 3: z score (past days only) | 59 |
| Both methods | 34 |

Streaming simulation over 1,004 days (January 2015 to September 2017).

## Next steps

- Use Apache Kafka (producer and consumer)
- Store the results in SAP HANA and build a dashboard
- Implement an adaptive threshold (EWMA) and compare it with the baselines
