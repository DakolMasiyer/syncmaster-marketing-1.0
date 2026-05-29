const { spawn } = require('child_process');

async function callTool(name, args = {}, fileKey = '') {
  const env = { ...process.env };
  if (fileKey) {
    env.FIGMA_FILE_KEY = fileKey;
  }
  
  // Note: FIGMA_ACCESS_TOKEN must be in the environment already or in .env
  // If not, this might fail. We'll see the output.
  
  const mcp = spawn('npx', ['-y', '@vkhanhqui/figma-mcp-go'], { env });
  
  return new Promise((resolve, reject) => {
    let output = '';
    mcp.stdout.on('data', d => {
      output += d.toString();
    });
    
    mcp.stderr.on('data', d => {
      console.error('STDERR:', d.toString());
    });

    const send = (msg) => {
      mcp.stdin.write(JSON.stringify(msg) + '\n');
    };

    send({ jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'agent', version: '1.0' } } });
    
    setTimeout(() => {
      send({ jsonrpc: '2.0', method: 'notifications/initialized', params: {} });
      
      setTimeout(() => {
        send({ jsonrpc: '2.0', id: 2, method: 'tools/call', params: { name, arguments: args } });
        
        setTimeout(() => {
          mcp.kill();
          resolve(output);
        }, 10000); // Wait 10s for response
      }, 1000);
    }, 1000);
  });
}

const toolName = process.argv[2] || 'get_pages';
const fileKey = process.argv[3] || 'vtkUJjxelIr8aypl079YHj';

callTool(toolName, {}, fileKey).then(out => {
  console.log(out);
}).catch(err => {
  console.error(err);
});
