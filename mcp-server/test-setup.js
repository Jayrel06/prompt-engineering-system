#!/usr/bin/env node

/**
 * Test Setup Script
 * Verifies that the MCP server is correctly configured before use with Claude Desktop
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PROJECT_ROOT = path.resolve(__dirname, '..');
const REQUIRED_DIRS = [
  'scripts',
  'context',
  'frameworks',
  'templates'
];
const REQUIRED_FILES = [
  'scripts/context-loader.py'
];

console.log('========================================');
console.log('MCP Server Setup Verification');
console.log('========================================\n');

let hasErrors = false;

// Check Node.js version
console.log('[1/6] Checking Node.js version...');
const nodeVersion = process.version;
const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);
if (majorVersion < 18) {
  console.log(`  ❌ Node.js ${nodeVersion} detected. Version 18+ required.`);
  hasErrors = true;
} else {
  console.log(`  ✅ Node.js ${nodeVersion}`);
}

// Check project structure
console.log('\n[2/6] Checking project structure...');
for (const dir of REQUIRED_DIRS) {
  const dirPath = path.join(PROJECT_ROOT, dir);
  if (fs.existsSync(dirPath)) {
    console.log(`  ✅ ${dir}/`);
  } else {
    console.log(`  ❌ Missing directory: ${dir}/`);
    hasErrors = true;
  }
}

// Check required files
console.log('\n[3/6] Checking required files...');
for (const file of REQUIRED_FILES) {
  const filePath = path.join(PROJECT_ROOT, file);
  if (fs.existsSync(filePath)) {
    console.log(`  ✅ ${file}`);
  } else {
    console.log(`  ❌ Missing file: ${file}`);
    hasErrors = true;
  }
}

// Check dependencies
console.log('\n[4/6] Checking npm dependencies...');
const nodeModulesPath = path.join(__dirname, 'node_modules');
const packageJsonPath = path.join(__dirname, 'package.json');

if (!fs.existsSync(packageJsonPath)) {
  console.log('  ❌ package.json not found');
  hasErrors = true;
} else if (!fs.existsSync(nodeModulesPath)) {
  console.log('  ❌ node_modules not found. Run: npm install');
  hasErrors = true;
} else {
  const mcpSdkPath = path.join(nodeModulesPath, '@modelcontextprotocol', 'sdk');
  if (fs.existsSync(mcpSdkPath)) {
    console.log('  ✅ @modelcontextprotocol/sdk installed');
  } else {
    console.log('  ❌ MCP SDK not found. Run: npm install');
    hasErrors = true;
  }
}

// Check build output
console.log('\n[5/6] Checking build output...');
const distPath = path.join(__dirname, 'dist');
const indexJsPath = path.join(distPath, 'index.js');

if (!fs.existsSync(distPath)) {
  console.log('  ❌ dist/ not found. Run: npm run build');
  hasErrors = true;
} else if (!fs.existsSync(indexJsPath)) {
  console.log('  ❌ dist/index.js not found. Run: npm run build');
  hasErrors = true;
} else {
  console.log('  ✅ dist/index.js exists');
}

// Check Python availability
console.log('\n[6/6] Checking Python availability...');
import { exec } from 'child_process';
exec('python --version', (error, stdout, stderr) => {
  if (error) {
    console.log('  ❌ Python not found in PATH');
    console.log('     The server requires Python 3 for context assembly.');
    hasErrors = true;
  } else {
    const version = stdout.trim() || stderr.trim();
    if (version.includes('Python 3')) {
      console.log(`  ✅ ${version}`);
    } else {
      console.log(`  ⚠️  ${version} - Python 3 recommended`);
    }
  }

  // Final summary
  console.log('\n========================================');
  if (hasErrors) {
    console.log('❌ SETUP INCOMPLETE');
    console.log('========================================\n');
    console.log('Please fix the errors above before using the MCP server.\n');
    console.log('Common fixes:');
    console.log('  - Run: npm install');
    console.log('  - Run: npm run build');
    console.log('  - Install Python 3 and add to PATH');
    console.log('  - Verify project structure\n');
    process.exit(1);
  } else {
    console.log('✅ ALL CHECKS PASSED');
    console.log('========================================\n');
    console.log('Your MCP server is ready to use!\n');
    console.log('Next steps:');
    console.log('1. Add to Claude Desktop config:');
    console.log(`   ${path.join(__dirname, 'claude_desktop_config.example.json')}`);
    console.log('\n2. Restart Claude Desktop');
    console.log('\n3. Test by asking:');
    console.log('   "List all available frameworks"\n');
    console.log('For detailed usage, see USAGE_EXAMPLES.md\n');
    process.exit(0);
  }
});
