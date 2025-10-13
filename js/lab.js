// js/lab.js
// Exports: runLabDemo(), AITeacher, reactionEnergy

// --- Small, safe math evaluator (shunting-yard + RPN) ---
const MathFunctions = {
  sin: Math.sin,
  cos: Math.cos,
  tan: Math.tan,
  asin: Math.asin,
  acos: Math.acos,
  atan: Math.atan,
  sqrt: Math.sqrt,
  log: Math.log, // natural log
  ln: Math.log,
  exp: Math.exp,
  abs: Math.abs,
  pow: Math.pow,
  PI: Math.PI,
  E: Math.E,
};

function tokenize(expr) {
  const tokens = [];
  const re = /\s*([A-Za-z_][A-Za-z0-9_]*|\d*\.?\d+(?:e[+\-]?\d+)?|[()+\-*/^,])\s*/ig;
  let m;
  while ((m = re.exec(expr)) !== null) tokens.push(m[1]);
  // simple validation: ensure entire string consumed
  const joined = tokens.join('');
  const stripped = expr.replace(/\s+/g,'');
  if (!stripped.toLowerCase().startsWith(joined.toLowerCase())) {
    // fallback: still return tokens but user might have unsupported chars
  }
  return tokens;
}

const opPrecedence = {
  '+': 2, '-': 2,
  '*': 3, '/': 3,
  '^': 4
};
const rightAssoc = {'^': true};

function toRPN(tokens) {
  const output = [];
  const ops = [];
  for (let i = 0; i < tokens.length; i++) {
    const t = tokens[i];
    if (!isNaN(Number(t))) {
      output.push(t);
      continue;
    }
    if (/^[A-Za-z_][A-Za-z0-9_]*$/.test(t)) {
      // function or constant
      ops.push(t);
      continue;
    }
    if (t === ',') {
      while (ops.length && ops[ops.length-1] !== '(') output.push(ops.pop());
      continue;
    }
    if (t in opPrecedence) {
      while (ops.length) {
        const top = ops[ops.length-1];
        if (top in opPrecedence &&
            ((rightAssoc[t] && opPrecedence[t] < opPrecedence[top]) ||
            (!rightAssoc[t] && opPrecedence[t] <= opPrecedence[top]))
        ) {
          output.push(ops.pop());
        } else break;
      }
      ops.push(t);
      continue;
    }
    if (t === '(') { ops.push(t); continue; }
    if (t === ')') {
      while (ops.length && ops[ops.length-1] !== '(') output.push(ops.pop());
      if (ops.length === 0) throw new Error("Mismatched parentheses");
      ops.pop(); // pop '('
      // if top is a function name, pop to output
      if (ops.length && /^[A-Za-z_]/.test(ops[ops.length-1])) output.push(ops.pop());
      continue;
    }
    throw new Error("Unknown token: " + t);
  }
  while (ops.length) {
    const o = ops.pop();
    if (o === '(' || o === ')') throw new Error("Mismatched parentheses");
    output.push(o);
  }
  return output;
}

function evalRPN(rpn) {
  const stack = [];
  for (const t of rpn) {
    if (!isNaN(Number(t))) { stack.push(Number(t)); continue; }
    if (t in MathFunctions) {
      // constant
      if (typeof MathFunctions[t] === 'number') stack.push(MathFunctions[t]);
      else {
        // function: pop one argument, support binary pow via pow()
        const a = stack.pop();
        if (a === undefined) throw new Error("Insufficient arguments for " + t);
        stack.push(MathFunctions[t](a));
      }
      continue;
    }
    if (/^[A-Za-z_][A-Za-z0-9_]*$/.test(t)) {
      // unknown identifier: maybe a function that needs 1 or 2 args (like pow)
      const name = t;
      if (name === 'pow') {
        const b = stack.pop(), a = stack.pop();
        if (a === undefined || b === undefined) throw new Error("Insufficient args for pow");
        stack.push(Math.pow(a,b));
        continue;
      }
      if (name === 'PI') { stack.push(Math.PI); continue; }
      if (name === 'E') { stack.push(Math.E); continue; }
      throw new Error("Unknown identifier: " + name);
    }
    // operators
    if (t === '+') {
      const b = stack.pop(), a = stack.pop(); stack.push(a + b); continue;
    }
    if (t === '-') {
      const b = stack.pop(), a = stack.pop(); stack.push(a - b); continue;
    }
    if (t === '*') {
      const b = stack.pop(), a = stack.pop(); stack.push(a * b); continue;
    }
    if (t === '/') {
      const b = stack.pop(), a = stack.pop(); stack.push(a / b); continue;
    }
    if (t === '^') {
      const b = stack.pop(), a = stack.pop(); stack.push(Math.pow(a, b)); continue;
    }
    throw new Error("Unsupported token in RPN: " + t);
  }
  if (stack.length !== 1) throw new Error("Invalid expression");
  return stack[0];
}

function safeEvaluate(expr) {
  if (typeof expr !== 'string') throw new Error("Expression must be a string");
  // reject suspicious characters
  if (/[^0-9A-Za-z_\.\^\+\-\*\/\(\)\,\s:eE]/.test(expr)) {
    throw new Error("Forbidden character in expression");
  }
  const tokens = tokenize(expr);
  const rpn = toRPN(tokens);
  return evalRPN(rpn);
}

// --- Chemistry: tiny formation enthalpy lookup (kJ/mol) ---
const formationEnthalpies = {
  // approximate standard enthalpies of formation (kJ/mol)
  "H2": 0.0,
  "O2": 0.0,
  "H2O": -241.8,
  "CO2": -393.5,
  "CH4": -74.8,
  "CO": -110.5,
  "O3": 142.7,
  "N2": 0.0,
  "NH3": -45.9,
  "H2O2": -187.8,
};

// reactants/products are objects like { H2: 2, O2:1 }
export function reactionEnergy(reactants = {}, products = {}) {
  let rSum = 0, pSum = 0;
  for (const k of Object.keys(reactants)) {
    const c = Number(reactants[k]) || 0;
    const val = formationEnthalpies[k] ?? 0;
    rSum += c * val;
  }
  for (const k of Object.keys(products)) {
    const c = Number(products[k]) || 0;
    const val = formationEnthalpies[k] ?? 0;
    pSum += c * val;
  }
  // ΔH = sum(products) - sum(reactants)
  return pSum - rSum;
}

// --- AITeacher: small helper with friendly responses ---
export const AITeacher = {
  explainFormula(expr) {
    try {
      const v = safeEvaluate(expr);
      return `I evaluated it safely and got ${v}. You used functions/constants like ${this._listUsed(expr)}.`;
    } catch (e) {
      return `I couldn't evaluate that: ${e.message}. Try simpler expressions or valid functions (sin, cos, sqrt, log, pow).`;
    }
  },
  safeEvaluate,
  _listUsed(expr) {
    const set = new Set();
    const tokens = tokenize(expr);
    for (const t of tokens) {
      if (/^[A-Za-z_]/.test(t)) set.add(t);
    }
    if (set.size === 0) return 'none';
    return [...set].join(', ');
  },
  suggestChemistry(react, prod, energy = null) {
    let s = '';
    if (energy === null) {
      s = 'I calculated a reaction energy (ΔH).';
    } else {
      s = (energy < 0) ? 'This reaction is likely exothermic.' : (energy > 0) ? 'This reaction is likely endothermic.' : 'ΔH is about zero.';
    }
    // heuristic tips
    s += ' Check stoichiometry and whether species are known (H2, O2, H2O, CO2, CH4).';
    return s;
  },
  guideQuantum(qstate) {
    // qstate is an array of two complex-like arrays [{re,im}, {re,im}] or simple reals
    const info = (typeof qstate[0] === 'number') ? qstate : qstate.map(c => `${c.re.toFixed(3)}${c.im?('+'+c.im.toFixed(3)+'i'):''}`);
    return `State amplitudes: ${info.join(', ')}. Try measuring or applying another gate (X, Z, H).`;
  },
  suggestNextStep(domain) {
    if (domain === 'quantum') return 'Try adding another gate (X or Z) or measuring repeatedly to see collapse statistics.';
    if (domain === 'chemistry') return 'Try changing stoichiometry or adding common molecules (CO2, CH4).';
    return 'Explore variations and observe how outputs change.';
  }
};

// --- demo runner ---
export function runLabDemo() {
  // small console message and visual greeting
  console.info("Aura Quantum Lab: demo started.");
  // return a friendly greeting in the page if needed
  const el = document.querySelector('header');
  if (el) {
    const p = document.createElement('p');
    p.style.color = 'var(--muted)';
    p.style.marginTop = '6px';
    p.textContent = 'AI Teacher active — try typing "sqrt(2)+pow(3,2)" into the math box.';
    el.appendChild(p);
  }
}
