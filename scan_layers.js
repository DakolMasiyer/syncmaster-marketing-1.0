const { spawn } = require('child_process');
async function run() {
  const mcp = spawn('npx', ['-y', '@vkhanhqui/figma-mcp-go']);
  const nodeIds = [
      '194:2639', '194:2667', '194:2696', '194:2724', '194:2766',
      '198:3022', '198:3023'
  ];
  const req = (id, method, params) => JSON.stringify({ jsonrpc: '2.0', id, method, params }) + '\n';
  mcp.stdin.write(req(1, 'initialize', { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'test', version: '1.0' } }));
  await new Promise(r => setTimeout(r, 2000));
  mcp.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized', params: {} }) + '\n');
  await new Promise(r => setTimeout(r, 2000));
  
  for (let i = 0; i < nodeIds.length; i++) {
      mcp.stdin.write(req(100 + i, 'tools/call', { name: 'scan_text_nodes', arguments: { nodeId: nodeIds[i] } }));
      await new Promise(r => setTimeout(r, 1000));
  }
  
  mcp.stdout.on('data', d => console.log(d.toString()));
  await new Promise(r => setTimeout(r, 5000));
  mcp.kill();
}
run();
