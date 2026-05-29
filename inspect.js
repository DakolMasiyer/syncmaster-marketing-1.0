const { spawn } = require('child_process');
async function run() {
  const mcp = spawn('npx', ['-y', '@vkhanhqui/figma-mcp-go']);
  mcp.stdout.on('data', d => console.log(d.toString()));
  const req = (id, method, params) => JSON.stringify({ jsonrpc: '2.0', id, method, params }) + '\n';
  mcp.stdin.write(req(1, 'initialize', { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'test', version: '1.0' } }));
  await new Promise(r => setTimeout(r, 2000));
  mcp.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized', params: {} }) + '\n');
  await new Promise(r => setTimeout(r, 2000));
  mcp.stdin.write(req(2, 'tools/call', { name: 'get_node', arguments: { nodeId: '8:551' } }));
  await new Promise(r => setTimeout(r, 5000));
  mcp.kill();
}
run();
