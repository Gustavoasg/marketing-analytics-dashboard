# 📊 Marketing Analytics Dashboard

Recreación del dashboard **Executive Summary** de Improvado, construida con Python + Streamlit.

## Dataset
- **Fuente:** [PPC Campaign Performance Data — Kaggle](https://www.kaggle.com/datasets/aashwinkumar/ppc-campaign-performance-data)
- **Registros:** 888 campañas (año 2024)
- **Métricas:** Spend, Impressions, CTR, CPC, Conversions, Conversion Rate, ROAS

## Stack
| Herramienta | Uso |
|---|---|
| `Streamlit` | Framework del dashboard |
| `Plotly` | Gráficas interactivas |
| `Pandas` | Procesamiento de datos |

## Cómo ejecutar localmente

```bash
# 1. Clonar el repo
git clone https://github.com/TU_USUARIO/marketing-analytics-dashboard.git
cd marketing-analytics-dashboard

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
streamlit run app.py
```

## Despliegue en Streamlit Cloud

1. Sube el repo a GitHub (con `app.py`, `marketing_data.csv`, `requirements.txt`)
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repo → selecciona `app.py` → Deploy

## Estructura del proyecto

```
📁 marketing-analytics-dashboard/
├── app.py                  # Dashboard principal
├── marketing_data.csv      # Dataset procesado (Kaggle)
├── requirements.txt        # Dependencias Python
└── README.md
```

## Componentes del Dashboard

- **8 KPI Cards** — Spend, CPM, CTR, CPC, Revenue, Impressions, Conversions, Conversion Rate
- **Gráfica de líneas** — Impresiones mensuales por canal (Programmatic, Paid Search, Paid Social, Organic)
- **Channel Performance Table** — Métricas agregadas por canal
- **Data Source Performance Table** — Métricas por plataforma (Facebook, Google, Instagram, LinkedIn, YouTube)
- **Campaign Performance Table** — Top 8 campañas por impresiones
- **Spend by Platform** — Bar chart horizontal
- **Conversions by Channel** — Donut chart

## Filtros interactivos

- Channel (multiselect)
- Data Source / Platform (multiselect)  
- Date Range (date picker)
