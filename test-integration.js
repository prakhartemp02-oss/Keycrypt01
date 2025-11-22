// Simple integration test to verify critical components are in place
const fs = require('fs');
const path = require('path');

console.log('🧪 KeyCrypt Integration Test\n');

// Test critical files exist
const criticalFiles = [
  'src/app/game/[game_id]/page.tsx',
  'backend/app/__init__.py',
  'docker-compose.yml',
  '.env.example',
  'database/init.sql',
  'src/components/GameBoard/GameBoard.tsx',
  'src/components/Keyboard/VirtualKeyboard.tsx',
  'src/components/Hints/HintPanel.tsx',
  'src/hooks/useApi.ts',
  'src/hooks/useGameState.ts',
  'src/types/game.ts',
  'src/lib/api.ts'
];

let filesPassed = 0;
criticalFiles.forEach(file => {
  if (fs.existsSync(file)) {
    console.log(`✅ ${file}`);
    filesPassed++;
  } else {
    console.log(`❌ ${file} - Missing!`);
  }
});

// Test backend import fix
console.log('\n🔍 Backend Import Check:');
const backendInitPath = 'backend/app/__init__.py';
if (fs.existsSync(backendInitPath)) {
  const content = fs.readFileSync(backendInitPath, 'utf8');
  if (content.includes('import os')) {
    console.log('✅ Backend import fix applied');
    filesPassed++;
  } else {
    console.log('❌ Backend import fix missing');
  }
} else {
  console.log('❌ Backend __init__.py not found');
}

// Test game route structure
console.log('\n🎮 Game Route Structure:');
const gameRoutePath = 'src/app/game/[game_id]/page.tsx';
if (fs.existsSync(gameRoutePath)) {
  const content = fs.readFileSync(gameRoutePath, 'utf8');
  const hasGameId = content.includes('gameId');
  const hasGameBoard = content.includes('GameBoard');
  const hasVirtualKeyboard = content.includes('VirtualKeyboard');
  const hasHintPanel = content.includes('HintPanel');

  if (hasGameId && hasGameBoard && hasVirtualKeyboard && hasHintPanel) {
    console.log('✅ Game route has all required components');
    filesPassed++;
  } else {
    console.log('❌ Game route missing components');
    console.log(`  - Game ID param: ${hasGameId ? '✅' : '❌'}`);
    console.log(`  - GameBoard: ${hasGameBoard ? '✅' : '❌'}`);
    console.log(`  - VirtualKeyboard: ${hasVirtualKeyboard ? '✅' : '❌'}`);
    console.log(`  - HintPanel: ${hasHintPanel ? '✅' : '❌'}`);
  }
}

// Test Docker configuration
console.log('\n🐳 Docker Configuration:');
if (fs.existsSync('docker-compose.yml')) {
  const content = fs.readFileSync('docker-compose.yml', 'utf8');
  const hasFrontend = content.includes('frontend:');
  const hasBackend = content.includes('backend:');
  const hasPostgres = content.includes('postgres:');
  const hasRedis = content.includes('redis:');

  if (hasFrontend && hasBackend && hasPostgres) {
    console.log('✅ Docker Compose has required services');
    filesPassed++;
    console.log(`  - Frontend: ${hasFrontend ? '✅' : '❌'}`);
    console.log(`  - Backend: ${hasBackend ? '✅' : '❌'}`);
    console.log(`  - PostgreSQL: ${hasPostgres ? '✅' : '❌'}`);
    console.log(`  - Redis: ${hasRedis ? '✅' : '❌'}`);
  } else {
    console.log('❌ Docker Compose missing services');
  }
}

// Test database schema
console.log('\n🗄️ Database Schema:');
if (fs.existsSync('database/init.sql')) {
  const content = fs.readFileSync('database/init.sql', 'utf8');
  const hasGames = content.includes('CREATE TABLE.*games');
  const hasAttempts = content.includes('CREATE TABLE.*game_attempts');
  const hasUsers = content.includes('CREATE TABLE.*users');
  const hasDictionary = content.includes('CREATE TABLE.*word_dictionary');

  if (hasGames && hasAttempts && hasUsers && hasDictionary) {
    console.log('✅ Database schema has required tables');
    filesPassed++;
  } else {
    console.log('❌ Database schema missing tables');
  }
}

// Test environment template
console.log('\n🔧 Environment Template:');
if (fs.existsSync('.env.example')) {
  const content = fs.readFileSync('.env.example', 'utf8');
  const hasDatabase = content.includes('DATABASE_URL');
  const hasFlask = content.includes('FLASK_ENV');
  const hasCORS = content.includes('CORS_ORIGINS');
  const hasNextApi = content.includes('NEXT_PUBLIC_API_URL');

  if (hasDatabase && hasFlask && hasCORS && hasNextApi) {
    console.log('✅ Environment template has required variables');
    filesPassed++;
  } else {
    console.log('❌ Environment template missing variables');
  }
}

// Results
const totalTests = criticalFiles.length + 5; // +5 for the additional checks
const percentage = Math.round((filesPassed / totalTests) * 100);

console.log(`\n📊 Results: ${filesPassed}/${totalTests} tests passed (${percentage}%)`);

if (percentage >= 90) {
  console.log('🎉 Excellent! KeyCrypt is ready for development.');
} else if (percentage >= 75) {
  console.log('✅ Good! Most components are in place.');
} else if (percentage >= 50) {
  console.log('⚠️ Some issues found. Review the failed tests above.');
} else {
  console.log('❌ Critical issues found. Please address the failed tests.');
}

console.log('\n🚀 Next Steps:');
console.log('1. Copy .env.example to .env and configure');
console.log('2. Run: docker-compose up -d');
console.log('3. Visit: http://localhost:3000');
console.log('4. Check: http://localhost:5000/health');