# Streamlit Cloud Deployment Guide

## 🚀 Deploy Coffeeverse to Streamlit Cloud

### Step 1: Access Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account

### Step 2: Deploy from GitHub
1. Click "New app"
2. Select "From existing repo"
3. Choose repository: `anix-lynch/coffeeverse`
4. Set main file path: `streamlit_app.py`
5. Click "Deploy"

### Step 3: Configure Secrets
1. In your Streamlit Cloud app, go to "Settings" → "Secrets"
2. Copy the following secrets (get values from your `.env.azure` file after deployment):

```toml
AZURE_STORAGE_ACCOUNT = "your_storage_account_name"
AZURE_STORAGE_KEY = "your_storage_account_key"
AZURE_COSMOS_URL = "https://your-cosmos-account.documents.azure.com:443/"
AZURE_COSMOS_KEY = "your_cosmos_account_key"
```

### Step 4: Redeploy
1. After adding secrets, click "Save"
2. The app will automatically redeploy with your Azure credentials

### Step 5: Access Your Live Dashboard
- Your app will be available at: `https://coffeeverse.streamlit.app`
- Share this URL for portfolio/demo purposes

## 📋 Pre-deployment Checklist

- ✅ GitHub repository: https://github.com/anix-lynch/coffeeverse
- ✅ `streamlit_app.py` exists and is properly configured
- ✅ `requirements.txt` has compatible dependencies
- ✅ `.streamlit/secrets.toml` template provided
- ✅ `packages.txt` for system dependencies

## 🎯 Expected Result

Once deployed, you'll have:
- **Live Dashboard**: Real-time Azure ETL monitoring
- **Professional Demo**: Showcase Azure cloud skills
- **Portfolio Ready**: Add to gozeroshot.dev

## 💡 Cost Impact

- **Streamlit Cloud**: FREE (community plan)
- **Azure Services**: $0/month (Free Tier)
- **Total Cost**: $0/month for demo purposes

## 🆘 Troubleshooting

**App fails to start:**
- Check secrets are properly configured
- Verify Azure resources are deployed and accessible

**Data not loading:**
- Ensure Azure credentials have correct permissions
- Check Cosmos DB has data (run ETL pipeline first)

**Import errors:**
- Dependencies should be compatible - contact if issues persist

---

**Status**: Ready for deployment following Distro Dojo rule ✅
