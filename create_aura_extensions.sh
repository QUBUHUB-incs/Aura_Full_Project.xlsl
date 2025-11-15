#!/bin/bash

# Base folder
BASE="aura_extensions"

# Declare folders and extensions
declare -A EXTENSIONS=(
  ["scripts"]="R fn macro ser"
  ["ai"]="mod pipe train infer"
  ["data"]="db knw cache"
  ["automation"]="xlsl xlsmath xlsquant xlsstat xlsopt"
  ["ui"]="panel wgt report export notify"
  ["integration"]="api scrap shell env"
)

# Placeholder README content
declare -A READMES=(
  ["R"]="# .R – Rule/Logic Scripts\nPurpose: Reusable rules or AI logic."
  ["fn"]="# .fn – Function Modules\nPurpose: Reusable callable functions."
  ["macro"]="# .macro – Macro Scripts\nPurpose: Automate multi-step tasks."
  ["ser"]="# .ser – Serialized Modules\nPurpose: Store objects, workflow states, checkpoints."
  ["mod"]="# .mod – AI Model Modules\nPurpose: Plug-in AI/LLM modules."
  ["pipe"]="# .pipe – AI Pipeline Modules\nPurpose: Chain AI or function modules."
  ["train"]="# .train – Training Modules\nPurpose: Train or finetune AI/ML models."
  ["infer"]="# .infer – Inference Modules\nPurpose: Run predictions using models."
  ["db"]="# .db – Data Storage Modules\nPurpose: Store structured datasets."
  ["knw"]="# .knw – Knowledge Modules\nPurpose: Store ontologies, vocabularies, knowledge graphs."
  ["cache"]="# .cache – Temporary Storage\nPurpose: Store intermediate results."
  ["xlsl"]="# .xlsl – Core Automation Modules\nPurpose: General workflow automation."
  ["xlsmath"]="# .xlsmath – Math Workflows\nPurpose: Algebra, calculus, matrices."
  ["xlsquant"]="# .xlsquant – Financial/Quant Workflows\nPurpose: Financial modeling, forecasting."
  ["xlsstat"]="# .xlsstat – Statistical Workflows\nPurpose: Probability, regression, statistics."
  ["xlsopt"]="# .xlsopt – Optimization Workflows\nPurpose: Linear programming, AI optimization."
  ["panel"]="# .panel – Dashboard Panels\nPurpose: Interactive UI panels."
  ["wgt"]="# .wgt – Widgets\nPurpose: Small UI components."
  ["report"]="# .report – Reports\nPurpose: Generate tables, summaries."
  ["export"]="# .export – Export Workflows\nPurpose: Output results to files or endpoints."
  ["notify"]="# .notify – Notifications\nPurpose: Send messages or alerts."
  ["api"]="# .api – API Connectors\nPurpose: Connect external APIs or services."
  ["scrap"]="# .scrap – Web Scraping\nPurpose: Extract data from websites."
  ["shell"]="# .shell – System Scripts\nPurpose: Run shell commands."
  ["env"]="# .env – Environment Config\nPurpose: Store variables, secrets, configs."
)

# Create folders, example files, and README
for parent in "${!EXTENSIONS[@]}"; do
  for sub in ${EXTENSIONS[$parent]}; do
    folder="$BASE/$parent/$sub"
    mkdir -p "$folder"
    
    # Example file
    example_file="$folder/example.$sub"
    echo "# Example file for $sub extension" > "$example_file"
    
    # README file
    readme_file="$folder/README.$sub.md"
    echo -e "${READMES[$sub]}" > "$readme_file"
  done
done

echo "✅ Aura extension starter pack created in '$BASE/'"
