# Operations Dashboard

A Streamlit dashboard for reviewing orders, revenue, customers, products, regions, and completion status.

## Run

```bash
pip install streamlit pandas
streamlit run app.py
```

The app opens with the included fictional sample data. You can upload another CSV with the same columns from the sidebar.

Required columns: `date`, `customer`, `region`, `product`, `quantity`, `unit_price`, and `status`.
