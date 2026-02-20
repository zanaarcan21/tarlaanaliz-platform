// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
// KR-071: CI adımlarında izlenebilir komut akışı korunur.

import { spawn } from 'node:child_process';

const task = process.argv[2];

/** @type {Record<string, string[]>} */
const COMMANDS = {
  lint: ['pnpm', ['lint']],
  format: ['pnpm', ['format:check']],
  'type-check': ['pnpm', ['type-check']],
  coverage: ['pnpm', ['test:coverage']],
  build: ['pnpm', ['build']],
  analyze: ['pnpm', ['analyze']],
  start: ['pnpm', ['start']],
  e2e: ['pnpm', ['test:e2e']],
  a11y: ['pnpm', ['test:a11y']]
};

if (!task || !(task in COMMANDS)) {
  console.error(`Unknown task: ${task ?? 'undefined'}`);
  process.exit(1);
}

const [command, args] = COMMANDS[task];
const child = spawn(command, args, {
  stdio: 'inherit',
  shell: process.platform === 'win32'
});

child.on('exit', (code) => {
  process.exit(code ?? 1);
});
