# Folder Restructure Plan - Industry Standard

## Current Issues:
❌ Mixed concerns (agents/, api/, core/ at root)
❌ No clear src/ directory
❌ Infrastructure mixed with application code
❌ No tests/ structure
❌ No docs/ folder

## Industry Standard Structure:

```
coffeeverse/
├── src/                          # All application code
│   ├── etl/                      # ETL pipeline code
│   │   ├── extract/
│   │   ├── transform/
│   │   └── load/
│   ├── functions/                # Azure Functions
│   └── app/                      # Streamlit app
├── infrastructure/               # IaC (Bicep, Terraform)
│   ├── bicep/
│   └── scripts/
├── dbt/                          # dbt transformations
│   ├── models/
│   └── tests/
├── data/                         # Data artifacts
│   ├── raw/
│   ├── processed/
│   └── schemas/
├── tests/                        # All tests
│   ├── unit/
│   └── integration/
├── docs/                         # Documentation
├── .github/workflows/            # CI/CD
├── docker/                       # Docker configs
├── requirements.txt
└── README.md
```

## Actions:
1. Create src/ directory
2. Move azure_function/ → src/functions/
3. Move streamlit_app.py → src/app/
4. Move deploy/ → infrastructure/
5. Move dbt_project/ → dbt/
6. Remove agents/, api/, core/ (not part of ETL)
7. Create proper tests/ structure
