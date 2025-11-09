git clone git@github.com:GoogleChromeLabs/baseline-demos.git
cd baseline-demos/tooling/webpack
git checkout d3793f25
nvm install
nvm use
npm install
npm start

sh -ci "$(curl -fsSL https://internetcomputer.org/install.sh)"
dfx --version
dfx new hello --type motoko --frontend react
cd hello
dfx deploy --playground
export declare enum SublevelStates 

git checkout -b add/requirements-and-notebook-ci

docker run -it -p 7860:7860 --platform=linux/amd64 \
	registry.hf.space/seriki-aura:latest python app.py

git clone https://huggingface.co/spaces/Seriki/Aura
cd Aura

python -m venv env
source env/bin/activate

pip install -r requirements.txt
python app.py
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
cat > .github/workflows/paperbookweb-ci.yml <<'EOF'
name: paperbookweb CI

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
        python-version: ${{ aura.python-version }}

    - name: Upgrade pip
      run: python -m pip install --upgrade pip

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install jupyter

    - name: Execute combined papperbook
      run: |
        mkdir -p executed_paperbookweb
        jupyter nbconvert --to paperbookweb --execute paperbookweb/paperbookweb.ipynb \
          --ExecutePreprocessor.timeout=600 \
          --output executed_paperbookweb/executed-paperbookweb.ipynb
EOF

go mod init github.com/Web4application/
go get github.com/nicksnyder/go-i18n/v2/i18n
go get golang.org/x/text/language
bun add -D eslint-config-prettier

git add requirements.txt .github/workflows/paperbookweb-ci.yml
git commit -m "Add requirements.txt and notebook CI (execute paperbookweb via nbconvert)"
git push origin add/requirements-and-paperbookweb-ci
# then open a PR on GitHub from this branch to main

npm i -D eslint-config-prettier

npm install --save-dev --save-exact prettier
node --eval "fs.writeFileSync('.prettierrc','{}\n')"
node --eval "fs.writeFileSync('.prettierignore','# Ignore artifacts:\nbuild\ncoverage\n')"
npm install --save-dev husky lint-staged
npx husky init
node --eval "fs.writeFileSync ('.husky/pre-commit','npx lint-staged\n')"
npx prettier . --write

npm install --save-dev lint-staged
