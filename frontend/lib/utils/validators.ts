// lib/utils/validators.ts
export const validatePythonCode = (code: string): { valid: boolean; error?: string } => {
  if (!code || code.trim() === '') {
    return { valid: false, error: 'Code cannot be empty' };
  }

  // Basic Python syntax checks
  if (code.includes('def ') && !code.includes(':')) {
    return { valid: false, error: 'Function definition missing colon' };
  }

  // Check for unmatched parentheses
  const parens = (code.match(/\(/g) || []).length;
  const closeParens = (code.match(/\)/g) || []).length;
  if (parens !== closeParens) {
    return { valid: false, error: 'Unmatched parentheses' };
  }

  return { valid: true };
};

export const validateModelName = (modelName: string): boolean => {
  return /^[a-zA-Z0-9_\-]+[:/][a-zA-Z0-9_\-]+$/.test(modelName);
};

export const validateTestCase = (testCase: string): { valid: boolean; error?: string } => {
  if (!testCase.startsWith('assert')) {
    return { valid: false, error: 'Test case must start with "assert"' };
  }

  if (testCase.includes('candidate') && !testCase.includes('solution')) {
    return { valid: true }; // Will be replaced at runtime
  }

  return { valid: true };
};