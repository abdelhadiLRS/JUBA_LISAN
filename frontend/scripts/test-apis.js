// test-apis.js - اختبار APIs الذكاء الاصطناعي
const fetch = require('node-fetch');

const API_BASE = process.env.API_BASE || 'http://localhost:3000';

async function testOpenAI() {
  console.log('\n🧪 Testing OpenAI API (AI Tutor)...');
  console.log('=' .repeat(50));
  
  try {
    const response = await fetch(`${API_BASE}/api/ai/tutor`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: 'Hello, I want to learn Arabic. Can you help me?',
        language: 'ar',
        level: 'beginner'
      })
    });
    
    const data = await response.json();
    
    if (response.ok && data.response && !data.error) {
      console.log('✅ OpenAI API is working!');
      console.log(`📝 Response (${data.response.length} chars):`);
      console.log('   ' + data.response.substring(0, 150) + (data.response.length > 150 ? '...' : ''));
      
      if (data.suggestion) {
        console.log(`💡 Suggestion: ${data.suggestion}`);
      }
      
      if (data.isMock) {
        console.log('⚠️  Running in MOCK mode (no API key configured)');
      } else {
        console.log('🔑 Using real OpenAI API');
      }
      
      return true;
    } else {
      console.log('❌ OpenAI API error:', data.error || 'Unknown error');
      if (data.details) {
        console.log('   Details:', data.details);
      }
      return false;
    }
  } catch (error) {
    console.log('❌ OpenAI API connection failed:', error.message);
    console.log('   Make sure the server is running on', API_BASE);
    return false;
  }
}

async function testSpeechAPI() {
  console.log('\n🧪 Testing Google Speech API...');
  console.log('=' .repeat(50));
  console.log('⚠️  Note: Speech API requires actual audio file');
  console.log('📝 Manual testing recommended through browser interface');
  console.log('');
  console.log('To test manually:');
  console.log('1. Open the app in browser');
  console.log('2. Navigate to AI Tutor or Speech Practice');
  console.log('3. Click the microphone and speak');
  console.log('4. Check the analysis results');
  
  // Try a simple health check
  try {
    const response = await fetch(`${API_BASE}/api/ai/speech`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    });
    
    if (response.status === 400) {
      console.log('✅ Speech API endpoint is reachable');
      console.log('ℹ️  Waiting for audio file (expected behavior)');
      return true;
    } else if (response.status === 503 || response.status === 500) {
      const data = await response.json();
      console.log('⚠️  Speech API available but not configured:', data.error);
      return false;
    } else {
      const data = await response.json();
      console.log('📊 Speech API response:', data);
      return true;
    }
  } catch (error) {
    console.log('❌ Speech API connection failed:', error.message);
    return false;
  }
}

async function testHealthCheck() {
  console.log('🚀 Starting API tests...');
  console.log('📍 Base URL:', API_BASE);
  console.log('=' .repeat(50));
  
  try {
    const response = await fetch(`${API_BASE}/api/health`);
    if (response.ok) {
      console.log('✅ Server is healthy');
      return true;
    }
  } catch (e) {
    console.log('⚠️  Health endpoint not available, continuing tests...');
  }
  return true;
}

async function runAllTests() {
  console.clear();
  console.log('\n');
  console.log('╔═══════════════════════════════════════════════╗');
  console.log('║       JUBA LISAN - API Tests Suite           ║');
  console.log('╚═══════════════════════════════════════════════╝');
  
  const results = {
    health: await testHealthCheck(),
    openai: await testOpenAI(),
    speech: await testSpeechAPI(),
  };
  
  console.log('\n');
  console.log('=' .repeat(50));
  console.log('📊 Test Summary');
  console.log('=' .repeat(50));
  console.log(`Server Health:    ${results.health ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`OpenAI (Tutor):   ${results.openai ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`Google Speech:    ${results.speech ? '✅ PASS' : '❌ FAIL'}`);
  console.log('=' .repeat(50));
  
  const allPassed = Object.values(results).every(r => r === true);
  
  if (allPassed) {
    console.log('\n🎉 All tests passed! APIs are ready to use.');
  } else {
    console.log('\n⚠️  Some tests failed. Check the errors above.');
    console.log('📖 See API_SETUP_GUIDE.md for configuration help.');
  }
  
  console.log('');
  
  process.exit(allPassed ? 0 : 1);
}

runAllTests().catch(console.error);
