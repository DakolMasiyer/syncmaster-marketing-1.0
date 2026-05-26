const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const NODES = {
  tokens: '66:3',
  guidelines: '10:906',
  carousel: '52:869'
};

const OUTPUT_DIR = __dirname;

function sanitizeNodeId(id) {
  return id.replace(/-/g, ':');
}

function parseMcpResponse(res) {
  if (res && res.content && Array.isArray(res.content)) {
    const textContent = res.content.find(c => c.type === 'text');
    if (textContent) {
      try {
        return JSON.parse(textContent.text);
      } catch (e) {
        return textContent.text;
      }
    }
  }
  return res;
}

async function run() {
  console.log('========================================================');
  console.log('SyncMaster Figma Design System Extractor');
  console.log('========================================================');
  console.log('Make sure Figma Desktop is open with your active file:');
  console.log('vtkUJjxelIr8aypl079YHj');
  console.log('And that the figma-mcp-go plugin is running inside it!');
  console.log('--------------------------------------------------------');
  
  const mcp = spawn('npx', ['-y', '@vkhanhqui/figma-mcp-go']);
  
  let buffer = '';
  const pendingRequests = new Map();
  let requestId = 1;
  
  mcp.stdout.on('data', (data) => {
    buffer += data.toString();
    let lines = buffer.split('\n');
    buffer = lines.pop();
    
    for (let line of lines) {
      if (!line.trim()) continue;
      try {
        const msg = JSON.parse(line);
        if (msg.id && pendingRequests.has(msg.id)) {
          const { resolve, reject } = pendingRequests.get(msg.id);
          pendingRequests.delete(msg.id);
          if (msg.error) {
            reject(msg.error);
          } else {
            resolve(msg.result);
          }
        }
      } catch (err) {
        // Suppress noise but log errors
      }
    }
  });
  
  mcp.stderr.on('data', (data) => {
    const log = data.toString().trim();
    if (log && !log.includes('debugger') && !log.includes('ws:')) {
      console.log('[figma-mcp-go]:', log);
    }
  });
  
  mcp.on('close', (code) => {
    console.log(`figma-mcp-go server exited with code ${code}`);
  });
  
  function sendRequest(method, params = {}) {
    const id = requestId++;
    return new Promise((resolve, reject) => {
      pendingRequests.set(id, { resolve, reject });
      const req = JSON.stringify({ jsonrpc: '2.0', id, method, params }) + '\n';
      mcp.stdin.write(req);
    });
  }
  
  function sendNotification(method, params = {}) {
    const req = JSON.stringify({ jsonrpc: '2.0', method, params }) + '\n';
    mcp.stdin.write(req);
  }
  
  async function callTool(name, args = {}) {
    console.log(`Calling tool "${name}"...`);
    const res = await sendRequest('tools/call', { name, arguments: args });
    return parseMcpResponse(res);
  }
  
  try {
    console.log('Initializing connection to MCP server...');
    const initRes = await sendRequest('initialize', {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: { name: 'syncmaster-extractor', version: '1.0.0' }
    });
    
    sendNotification('notifications/initialized');
    console.log('Protocol handshake completed. Waiting for Figma connection...');
    await new Promise(r => setTimeout(r, 4000));
    
    // 1. Get variable defs
    const variables = await callTool('get_variable_defs');
    fs.writeFileSync(
      path.join(OUTPUT_DIR, 'figma-variables-raw.json'),
      JSON.stringify(variables, null, 2)
    );
    console.log('✅ Extracted and saved: figma-variables-raw.json');
    
    // 2. Get style defs
    const styles = await callTool('get_styles');
    fs.writeFileSync(
      path.join(OUTPUT_DIR, 'figma-styles-raw.json'),
      JSON.stringify(styles, null, 2)
    );
    console.log('✅ Extracted and saved: figma-styles-raw.json');
    
    // 3. Get design system node (66:3)
    const tokensNode = await callTool('get_node', { id: sanitizeNodeId(NODES.tokens) });
    fs.writeFileSync(
      path.join(OUTPUT_DIR, 'figma-node-tokens.json'),
      JSON.stringify(tokensNode, null, 2)
    );
    console.log('✅ Extracted and saved: figma-node-tokens.json');
    
    // 4. Get brand guidelines node (10:906)
    const guidelinesNode = await callTool('get_node', { id: sanitizeNodeId(NODES.guidelines) });
    fs.writeFileSync(
      path.join(OUTPUT_DIR, 'figma-node-guidelines.json'),
      JSON.stringify(guidelinesNode, null, 2)
    );
    console.log('✅ Extracted and saved: figma-node-guidelines.json');
    
    // 5. Get carousel node (52:869)
    const carouselNode = await callTool('get_node', { id: sanitizeNodeId(NODES.carousel) });
    fs.writeFileSync(
      path.join(OUTPUT_DIR, 'figma-node-carousel.json'),
      JSON.stringify(carouselNode, null, 2)
    );
    console.log('✅ Extracted and saved: figma-node-carousel.json');
    
    console.log('--------------------------------------------------------');
    console.log('Extraction complete! All raw figma files are saved.');
    console.log('Next step: Run python3 merge-tokens.py to generate unified tokens.json');
    console.log('========================================================');
  } catch (err) {
    console.error('❌ Error during extraction:', err);
  } finally {
    mcp.kill();
  }
}

run();
