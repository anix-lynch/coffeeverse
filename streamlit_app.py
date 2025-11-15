"""
Streamlit Dashboard for Coffeeverse ETL Pipeline Monitoring
==========================================================

A real-time dashboard to monitor the Azure ETL pipeline performance,
data quality metrics, and business insights from the cocktail dataset.

Features:
- ETL pipeline status monitoring
- Data quality metrics visualization
- Cocktail analytics and insights
- Real-time Azure service metrics
- Cost monitoring and optimization tips

Deploy to Streamlit Cloud for free hosting.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import logging
import os
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
from azure.core.exceptions import ResourceNotFoundError, ServiceRequestError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Coffeeverse ETL Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Azure clients
@st.cache_resource
def init_azure_clients():
    """Initialize Azure clients with error handling."""
    try:
        # Get credentials from Streamlit secrets or environment
        account_name = st.secrets.get("AZURE_STORAGE_ACCOUNT", os.environ.get("AZURE_STORAGE_ACCOUNT"))
        account_key = st.secrets.get("AZURE_STORAGE_KEY", os.environ.get("AZURE_STORAGE_KEY"))
        cosmos_url = st.secrets.get("AZURE_COSMOS_URL", os.environ.get("AZURE_COSMOS_URL"))
        cosmos_key = st.secrets.get("AZURE_COSMOS_KEY", os.environ.get("AZURE_COSMOS_KEY"))

        if not all([account_name, account_key, cosmos_url, cosmos_key]):
            st.error("⚠️ Azure credentials not configured. Add them in Streamlit Cloud Secrets.")
            return None, None

        # Initialize Blob Storage client
        blob_client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=account_key
        )

        # Initialize Cosmos DB client
        cosmos_client = CosmosClient(cosmos_url, credential=cosmos_key)

        return blob_client, cosmos_client
    except Exception as e:
        st.error(f"Failed to initialize Azure clients: {e}")
        return None, None

blob_client, cosmos_client = init_azure_clients()

def load_css():
    """Load custom CSS for better styling."""
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
    .status-error {
        color: #d32f2f;
        font-weight: bold;
    }
    .status-warning {
        color: #ff9800;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def get_etl_status():
    """Get the current ETL pipeline status."""
    try:
        # Check recent blob containers for pipeline activity
        containers_to_check = [
            'coffeeverse-raw-data',
            'coffeeverse-processed-data',
            'coffeeverse-dbt-data'
        ]

        latest_activity = None
        total_blobs = 0

        for container_name in containers_to_check:
            try:
                container_client = blob_client.get_container_client(container_name)
                blobs = list(container_client.list_blobs())
                total_blobs += len(blobs)

                for blob in blobs:
                    blob_time = blob.last_modified
                    if latest_activity is None or blob_time > latest_activity:
                        latest_activity = blob_time
            except ResourceNotFoundError:
                continue  # Container might not exist yet
            except ServiceRequestError:
                continue

        if latest_activity:
            time_diff = datetime.now(latest_activity.tzinfo) - latest_activity
            if time_diff < timedelta(hours=1):
                return "🟢 ACTIVE", f"Last activity: {latest_activity.strftime('%Y-%m-%d %H:%M:%S')}"
            elif time_diff < timedelta(hours=24):
                return "🟡 IDLE", f"Last activity: {latest_activity.strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                return "🔴 INACTIVE", f"Last activity: {latest_activity.strftime('%Y-%m-%d %H:%M:%S')}"

        return "🔵 NOT STARTED", "No pipeline activity detected"

    except Exception as e:
        logger.error(f"Error checking ETL status: {e}")
        return "❌ ERROR", f"Unable to check status: {e}"

def get_cocktail_metrics():
    """Get cocktail dataset metrics from Cosmos DB."""
    try:
        if not cosmos_client:
            return 0, pd.DataFrame()

        # Get database and container
        database = cosmos_client.get_database_client("coffeeverse-db")
        container = database.get_container_client("cocktails")

        # Query for count
        query = "SELECT VALUE COUNT(1) FROM c"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        total_cocktails = items[0] if items else 0

        # Get sample data for analysis
        query = "SELECT TOP 100 * FROM c ORDER BY c._ts DESC"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))

        if items:
            df = pd.DataFrame([{
                'id': item.get('id', ''),
                'name': item.get('name', 'Unknown'),
                'category': item.get('category', 'Unknown'),
                'spirit_type': item.get('spirit_type', 'Unknown'),
                'complexity_score': float(item.get('complexity_score', 0)),
                'estimated_calories': int(item.get('estimated_calories', 0)),
                'is_alcoholic': item.get('is_alcoholic', False),
                'processed_at': item.get('processed_at', '')
            } for item in items])

            return total_cocktails, df

    except Exception as e:
        logger.error(f"Error querying Cosmos DB: {e}")

    return 0, pd.DataFrame()

def create_metrics_charts(df):
    """Create interactive charts for cocktail metrics."""
    if df.empty:
        return None, None, None

    # Spirit type distribution
    spirit_chart = px.pie(
        df,
        names='spirit_type',
        title='Cocktail Distribution by Spirit Type',
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    # Complexity distribution
    complexity_chart = px.histogram(
        df,
        x='complexity_score',
        nbins=10,
        title='Cocktail Complexity Distribution',
        labels={'complexity_score': 'Complexity Score', 'count': 'Number of Cocktails'}
    )

    # Calories vs Complexity scatter plot
    scatter_chart = px.scatter(
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

    return spirit_chart, complexity_chart, scatter_chart

def get_cost_estimate():
    """Provide rough cost estimates based on usage."""
    # These are rough estimates - in production you'd use Azure Cost Management API
    estimates = {
        'Blob Storage': '$0.02/month (Free tier)',
        'Cosmos DB': '$0.008/hour (Free tier)',
        'Functions': '$0.20/month (Free tier)',
        'Data Factory': '$0.75/month (Free tier)',
        'Synapse Analytics': '$0.01/month (Pay per query)',
        'Total Estimated': '$1.00/month'
    }
    return estimates

def main():
    """Main dashboard function."""
    load_css()

    # Header
    st.title("☕ Coffeeverse Azure ETL Pipeline Dashboard")
    st.caption("Real-time monitoring for Azure-native serverless ETL: Blob Storage → Functions → Data Factory → Cosmos DB | Orchestrated with Azure services")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("🔧 Controls")

        if st.button("🔄 Refresh Data"):
            st.rerun()

        st.markdown("---")
        st.markdown("### 📊 Pipeline Status")

        status, details = get_etl_status()
        if "ACTIVE" in status:
            st.markdown(f"<p class='status-success'>{status}</p>", unsafe_allow_html=True)
        elif "IDLE" in status:
            st.markdown(f"<p class='status-warning'>{status}</p>", unsafe_allow_html=True)
        elif "ERROR" in status:
            st.markdown(f"<p class='status-error'>{status}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p>{status}</p>", unsafe_allow_html=True)

        st.caption(details)

        st.markdown("---")
        st.markdown("### 💰 Cost Estimate")
        costs = get_cost_estimate()
        for service, cost in costs.items():
            st.caption(f"{service}: {cost}")

    # Main content
    col1, col2, col3, col4 = st.columns(4)

    # Get metrics
    total_cocktails, df = get_cocktail_metrics()

    with col1:
        st.metric("📊 Total Cocktails", f"{total_cocktails:,}")

    with col2:
        avg_complexity = df['complexity_score'].mean() if not df.empty else 0
        st.metric("🎯 Avg Complexity", f"{avg_complexity:.1f}")

    with col3:
        avg_calories = df['estimated_calories'].mean() if not df.empty else 0
        st.metric("🔥 Avg Calories", f"{avg_calories:.0f}")

    with col4:
        spirit_types = df['spirit_type'].nunique() if not df.empty else 0
        st.metric("🥃 Spirit Types", spirit_types)

    st.markdown("---")

    # Charts section
    if not df.empty:
        st.header("📈 Analytics Dashboard")

        tab1, tab2, tab3 = st.tabs(["Spirit Distribution", "Complexity Analysis", "Calories vs Complexity"])

        spirit_chart, complexity_chart, scatter_chart = create_metrics_charts(df)

        with tab1:
            if spirit_chart:
                st.plotly_chart(spirit_chart, use_container_width=True)

        with tab2:
            if complexity_chart:
                st.plotly_chart(complexity_chart, use_container_width=True)

        with tab3:
            if scatter_chart:
                st.plotly_chart(scatter_chart, use_container_width=True)

        # Data table
        st.markdown("---")
        st.header("📋 Recent Cocktails")
        st.dataframe(
            df[['name', 'spirit_type', 'complexity_score', 'estimated_calories', 'is_alcoholic']]
            .sort_values('complexity_score', ascending=False)
            .head(10),
            use_container_width=True
        )
    else:
        st.info("📝 No cocktail data available yet. Run the ETL pipeline to populate the dashboard.")

    # Pipeline information
    st.markdown("---")
    st.header("🔄 ETL Pipeline Information")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📁 Data Sources")
        st.markdown("""
        - **Raw Data**: Blob Storage (`coffeeverse-raw-data`)
        - **Processed Data**: Blob Storage (`coffeeverse-processed-data`)
        - **Analytics**: Synapse Analytics (`coffeeverse-dbt-data`)
        - **Operational**: Cosmos DB (`coffeeverse-db/cocktails`)
        """)

    with col2:
        st.subheader("⚙️ Pipeline Components")
        st.markdown("""
        - **Extract**: Blob Storage + External APIs
        - **Transform**: Azure Functions (Python)
        - **Load**: Cosmos DB + Blob Storage
        - **Model**: dbt-core + Synapse Analytics
        - **Orchestrate**: Azure Data Factory
        """)

    # Footer
    st.markdown("---")
    st.caption("☕ Coffeeverse ETL Pipeline - Built with Azure, Data Factory, dbt, and Streamlit")
    st.caption("Free Tier Compliant • Serverless • Scalable")

if __name__ == "__main__":
    main()
