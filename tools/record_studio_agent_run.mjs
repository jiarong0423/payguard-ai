#!/usr/bin/env node
// Operator-run: record one real run of AG Studio's built-in agents for the hosted dashboard to replay.
//
// Needs the local console in live mode with a Gemini key, e.g. in one terminal:
//   PAYGUARD_STUDIO_AGENTS=gemini PAYGUARD_GEMINI_TRANSPORT=api_key GEMINI_API_KEY=... PAYGUARD_GUIDE_MODEL=off \
//     ./tools/run.sh console
// (the Gemini profile venv must exist, see README), then in another terminal:
//   node tools/record_studio_agent_run.mjs [--url http://127.0.0.1:8000] [--question "..."]...
//
// It opens /dashboard.html?record=1 in headless Chromium, refuses to run unless the console reports the built-in
// agents as live, asks each question through the dashboard's AI panel (the evidence auditor hands questions
// outside its own set to Studio's lead agent), waits for each run to finish, and writes
// frontend/src/data/studio_agent_run_v1.json: the questions, every Studio tool call with its arguments, the final
// replies, timings and the final page layout. The key never reaches the browser, so it cannot be in the file;
// the file is validated (closed schema, no personal data, no key-like strings) before it is written.
// Nothing here runs in tests or in the hosted demo.
import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import { validateRecording } from '../frontend/src/dashboard/agentRecording.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const OUTPUT = resolve(projectRoot, 'frontend/src/data/studio_agent_run_v1.json');
const DEFAULT_QUESTIONS = ['Make a widget comparing cases by days to due'];
const RUN_TIMEOUT_MS = 240000;

function parseArguments(argv) {
  const options = { url: 'http://127.0.0.1:8000', questions: [] };
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === '--url') options.url = argv[++index];
    else if (argv[index] === '--question') options.questions.push(argv[++index]);
    else throw new Error(`unknown argument ${argv[index]}`);
  }
  if (!/^http:\/\/(127\.0\.0\.1|localhost):\d+$/u.test(options.url)) throw new Error('record only against the local console');
  if (!options.questions.length) options.questions = DEFAULT_QUESTIONS;
  return options;
}

async function main() {
  const options = parseArguments(process.argv.slice(2));
  const { chromium } = createRequire(import.meta.url)('playwright');
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    await page.goto(`${options.url}/dashboard.html?record=1`);
    await page.getByTestId('widget-deadline').waitFor({ timeout: 60000 });
    const mode = await page.getByTestId('dashboard-built-in').getAttribute('data-mode');
    if (mode !== 'live') throw new Error(`the console reports built-in agents "${mode}"; start it in live mode (see the header of this file)`);
    await page.getByTestId('dashboard-mode').click();
    const box = page.getByPlaceholder('Ask the AI Assistant...');
    for (const [index, question] of options.questions.entries()) {
      await box.fill(question);
      await box.press('Enter');
      // The auditor's reply after delegating ends with this sentence; one per question.
      await page.getByText(/handed it to Studio's lead agent/).nth(index).waitFor({ timeout: RUN_TIMEOUT_MS });
      console.log(`recorded: ${question}`);
    }
    const recording = await page.evaluate(() => window.__payguardRecorder.finish());
    validateRecording(recording);
    mkdirSync(dirname(OUTPUT), { recursive: true });
    writeFileSync(OUTPUT, `${JSON.stringify(recording, null, 2)}\n`);
    const steps = recording.runs.reduce((sum, run) => sum + run.steps.length, 0);
    console.log(`wrote ${OUTPUT}: ${recording.runs.length} run(s), ${steps} Studio tool calls. Review it, rebuild the frontend and commit it.`);
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(`record_studio_agent_run: ${error.message}`);
  process.exit(1);
});
