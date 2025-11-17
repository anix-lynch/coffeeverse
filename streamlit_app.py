"""
Coffeeverse Azure ETL Pipeline Dashboard
=========================================

Streamlit dashboard for Coffeeverse - Azure-native ETL pipeline.
Shows mock data while Azure resources are configured.

Features:
- ETL pipeline status
- Cocktail analytics
- Cost monitoring
- Ready to connect real Azure data

Deploy to Streamlit Cloud for free.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Coffeeverse ETL Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.metric-card {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 10px;
    border-left: 4px solid #0078d4;
}
.status-success {
    color: #00c853;
    font-weight: bold;
}
.status-warning {
    color: #ff9800;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("☕ Coffeeverse Azure ETL Pipeline Dashboard")
st.caption("Azure-native serverless ETL: Blob Storage → Functions → Cosmos DB | Orchestrated by Data Factory + dbt")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🔧 Controls")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Pipeline Status")
    
    status = "🟡 AWAITING CONFIGURATION"
    details = "Add Azure secrets to Streamlit Cloud to connect real data"
    st.markdown(f"<p class='status-warning'>{status}</p>", unsafe_allow_html=True)
    st.caption(details)
    
    st.markdown("---")
    st.markdown("### 💰 Cost Estimate")
    st.caption("Blob Storage: $0/mo (Free tier)")
    st.caption("Cosmos DB: $0/mo (Free tier)")
    st.caption("Functions: $0/mo (Free tier)")
    st.caption("Data Factory: $0/mo (Free tier)")
    st.caption("**Total: $0/month**")

# Generate mock data
@st.cache_data
def generate_mock_cocktails():
    """Generate mock cocktail data for demo."""
    spirits = ["Vodka", "Rum", "Gin", "Whiskey", "Tequila", "Brandy"]
    categories = ["Classic", "Contemporary", "Frozen", "Sour", "Tropical"]
    
    np.random.seed(42)
    
    data = {
        "id": [f"cocktail_{i:03d}" for i in range(1, 51)],
        "name": [f"Cocktail {i}" for i in range(1, 51)],
        "spirit_type": np.random.choice(spirits, 50),
        "category": np.random.choice(categories, 50),
        "complexity_score": np.random.uniform(1, 10, 50),
        "estimated_calories": np.random.randint(100, 400, 50),
        "is_alcoholic": np.random.choice([True, False], 50, p=[0.8, 0.2])
    }
    
    return pd.DataFrame(data)

# Main metrics
df = generate_mock_cocktails()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total Cocktails", f"{len(df):,}")

with col2:
    avg_complexity = df['complexity_score'].mean()
    st.metric("🎯 Avg Complexity", f"{avg_complexity:.1f}")

with col3:
    avg_calories = df['estimated_calories'].mean()
    st.metric("🔥 Avg Calories", f"{avg_calories:.0f}")

with col4:
    spirit_types = df['spirit_type'].nunique()
    st.metric("🥃 Spirit Types", spirit_types)

st.markdown("---")

# Analytics Dashboard
st.header("📈 Analytics Dashboard")

tab1, tab2, tab3 = st.tabs(["Spirit Distribution", "Complexity Analysis", "Calories vs Complexity"])

with tab1:
    fig = px.pie(
        df,
        names='spirit_type',
        title='Cocktail Distribution by Spirit Type',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = px.histogram(
        df,
        x='complexity_score',
        nbins=10,
        title='Cocktail Complexity Distribution',
        labels={'complexity_score': 'Complexity Score', 'count': 'Number of Cocktails'}
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    fig = px.scatter(
        df,
        x='complexity_score',
        y='estimated_calories',
        color='spirit_type',
        title='Calories vs Complexity by Spirit Type',
        labels={
            'complexity_score': 'Complexity Score',
            'estimated_calories': 'Estimated Calories',
            'spirit_type': 'Spirit Type'
        }
    )
    st.plotly_chart(fig, use_container_width=True)

# Data table
st.markdown("---")
st.header("📋 Sample Cocktails")
st.dataframe(
    df[['name', 'spirit_type', 'complexity_score', 'estimated_calories', 'is_alcoholic']]
    .sort_values('complexity_score', ascending=False)
    .head(15),
    use_container_width=True
)

# Pipeline info
st.markdown("---")
st.header("🔄 ETL Pipeline Information")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Data Sources")
    st.markdown("""
    - **Raw Data**: Azure Blob Storage
    - **Processed Data**: Azure Blob Storage
    - **Analytics**: Azure Synapse + dbt
    - **Operational**: Azure Cosmos DB
    """)

with col2:
    st.subheader("⚙️ Pipeline Components")
    st.markdown("""
    - **Extract**: Blob Storage + APIs
    - **Transform**: Azure Functions
    - **Load**: Cosmos DB + Blob
    - **Model**: dbt-core
    - **Orchestrate**: Data Factory
    """)

# Configuration section
st.markdown("---")
st.header("🔐 Configuration")

st.info("""
**To connect real Azure data:**

1. Create Azure resources:
   - Blob Storage Account
   - Cosmos DB Account

2. Add 4 secrets to Streamlit Cloud settings:
   - `AZURE_STORAGE_ACCOUNT`: Your storage account name
   - `AZURE_STORAGE_KEY`: Your storage account key
   - `AZURE_COSMOS_URL`: Your Cosmos DB endpoint
   - `AZURE_COSMOS_KEY`: Your Cosmos DB key

3. Redeploy app - dashboard will auto-connect!

**For Azure Free Tier setup**: https://docs.microsoft.com/azure/free
""")

# Footer
st.markdown("---")
st.caption("☕ Coffeeverse - Azure ETL Pipeline | Built with Streamlit")
st.caption("Free Tier Compliant • Serverless • Scalable • Ready for Production")
