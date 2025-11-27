const puppeteer = require('puppeteer');
require('dotenv').config(); // load .env variables
// --- CONFIG ---
// Use environment variable if available, else fallback to localhost
const INITIAL_URL = process.env.AURA_URL || 'http://localhost:3000';
const HEADLESS = process.env.HEADLESS === 'true' || false;

// --- MODEL CONFIG ---
const models = [
  { level: 1, name: "KLM" }, { level: 2, name: "FLM" }, { level: 3, name: "CLX" },
  { level: 4, name: "QLM" }, { level: 5, name: "AXT" }, { level: 6, name: "NXT" },
  { level: 7, name: "ZLM" }, { level: 8, name: "BLM" }, { level: 9, name: "OLM" },
  { level: 10, name: "LFX" }, { level: 11, name: "CXP" }, { level: 12, name: "PNX" },
  { level: 13, name: "VTX" }, { level: 14, name: "REX" }, { level: 15, name: "AXR" },
  { level: 16, name: "QPX" }, { level: 17, name: "SYX" }, { level: 18, name: "ORX" },
  { level: 19, name: "CRX" }, { level: 20, name: "OMEGA" },
  { level: 21, name: "QL1" }, { level: 22, name: "QL2" }, { level: 23, name: "QL3" },
  { level: 24, name: "M1" }, { level: 25, name: "M2" }, { level: 26, name: "M3" }
];

const levelThresholds = [
  50,100,150,200,250,300,350,400,450,500,
  550,600,650,700,750,800,850,900,950,1000,
  1200,1400,1600,1800,2000,2500
];

// --- MODEL STATE ---
let modelState = {
  level: 1,
  name: "KLM",
  performanceScore: 0,
  upvotes: 0,
  tasksCompleted: 0,
  shortMemory: [],
  longMemory: [],
  subAIs: []
};

// --- HELPER FUNCTIONS ---
function getModelForLevel(level) {
  return models.find(m => m.level === level) || models[models.length - 1];
}

function brainCapacityPercent(level) {
  return Math.floor((level / models.length) * 100);
}

function unlockModulesForLevel(level) {
  if(level >= 6) console.log("💡 Embeddings enabled");
  if(level >= 10) console.log("💡 Autonomous learning enabled");
  if(level >= 16) console.log("💡 NeoMind + XLSL integration");
  if(level >= 21) console.log("💡 Quantum-level reasoning unlocked");
  if(level >= 24) console.log("💡 Matrix-level multi-dimensional reasoning unlocked");
}

function checkEvolution() {
  const score = modelState.performanceScore;
  if(modelState.level < models.length && score >= levelThresholds[modelState.level - 1]) {
    modelState.level += 1;
    modelState.name = getModelForLevel(modelState.level).name;
    console.log(`✨ Aura evolved to ${modelState.name} (Level ${modelState.level})`);
    console.log(`🧠 Brain capacity: ${brainCapacityPercent(modelState.level)}%`);
    unlockModulesForLevel(modelState.level);
  }
}

// --- Sub-AI Class ---
class SubAI {
  constructor(name, skillLevel) {
    this.name = name;
    this.skillLevel = skillLevel;
    this.performanceScore = 0;
  }

  performTask(task) {
    const gain = Math.floor(Math.random() * 10 + this.skillLevel);
    this.performanceScore += gain;
    console.log(`⚡ Sub-AI ${this.name} completed "${task}" | Gain: ${gain}`);
    return gain;
  }
}

// --- Task Simulation ---
function completeTask(taskDescription, intelligenceGain = 10, upvote = false) {
  let gain = intelligenceGain;

  // Quantum multiplier
  if(modelState.level >= 21 && modelState.level <= 23) gain *= 1.5;
  // Matrix multiplier
  if(modelState.level >= 24) gain *= 2;

  modelState.performanceScore += gain;
  if(upvote) modelState.performanceScore += 5;
  modelState.tasksCompleted += 1;

  // Memory update
  modelState.shortMemory.push(taskDescription);
  if(modelState.shortMemory.length > 10) modelState.shortMemory.shift();
  if(modelState.performanceScore % 100 === 0) modelState.longMemory.push(taskDescription);

  // Matrix Levels spawn sub-AIs
  if(modelState.level >= 24 && modelState.subAIs.length < 3) {
    const subAI = new SubAI(`SubAI-${modelState.subAIs.length + 1}`, modelState.level);
    modelState.subAIs.push(subAI);
    console.log(`🤖 Spawned ${subAI.name} for multi-agent task`);
  }

  // Sub-AIs contribute
  modelState.subAIs.forEach(sub => {
    const subGain = sub.performTask(taskDescription);
    modelState.performanceScore += subGain * 0.5;
  });

  console.log(`💬 Task: "${taskDescription}" | Gain: ${gain} | Total Score: ${modelState.performanceScore}`);
  checkEvolution();
}

// --- Puppeteer Automation ---
(async () => {
  const browser = await puppeteer.launch({ headless: HEADLESS, defaultViewport: null, args: ['--start-maximized'] });
  const page = await browser.newPage();

  console.log(`🚀 Opening Aura at ${INITIAL_URL}...`);
  await page.goto(INITIAL_URL, { waitUntil: 'networkidle2' });

  await page.waitForSelector('#model-select');
  await page.select('#model-select', modelState.name);
  console.log(`🧠 Model loaded: ${modelState.name} (Level ${modelState.level})`);

  const messages = [
    "Hello Aura, test connection",
    "Run XLSL analysis",
    "Show me model capabilities",
    "Perform predictive reasoning",
    "Simulate multi-dimensional problem"
  ];

  // Continuous loop
  while(true) {
    for(const msg of messages) {
      await page.type('#input', msg, { delay: 40 });
      await page.click('#send');
      const intelligenceGain = Math.floor(Math.random() * 20 + 5);
      const upvote = Math.random() > 0.7;
      completeTask(msg, intelligenceGain, upvote);
      await page.waitForTimeout(3000);
    }
  }
})();
