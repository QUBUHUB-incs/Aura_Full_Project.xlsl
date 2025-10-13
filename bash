sh -ci "$(curl -fsSL https://internetcomputer.org/install.sh)"
dfx --version
dfx new hello --type motoko --frontend react
cd hello
dfx deploy --playground
export declare enum SublevelStates 

git checkout -b add/requirements-and-notebook-ci

# create requirements.txt with the content above
cat > requirements.txt <<'EOF'
pandas>=2.0
numpy>=1.24
matplotlib>=3.6
seaborn>=0.12
ipython
notebook
nbconvert
pytest
nbval
EOF

# create workflow file
mkdir -p .github/workflows
cat > .github/workflows/notebook-ci.yml <<'EOF'
name: Notebook CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  execute-notebook:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10]

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Upgrade pip
      run: python -m pip install --upgrade pip

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install jupyter

    - name: Execute combined notebook
      run: |
        mkdir -p executed_notebooks
        jupyter nbconvert --to notebook --execute notebook/Notebook.ipynb \
          --ExecutePreprocessor.timeout=600 \
          --output executed_notebooks/executed-Notebook.ipynb
EOF

git add requirements.txt .github/workflows/notebook-ci.yml
git commit -m "Add requirements.txt and notebook CI (execute notebook via nbconvert)"
git push origin add/requirements-and-notebook-ci
# then open a PR on GitHub from this branch to main
