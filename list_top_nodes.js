const fs = require('fs');

const content = fs.readFileSync(process.argv[2], 'utf8');
const matches = content.match(/\{"jsonrpc":"2.0","id":2,"result":\{"content":\[\{"type":"text","text":"(.*?)"\}\],"isError":false\}\}/);

if (!matches) {
  process.exit(1);
}

const data = JSON.parse(JSON.parse('"' + matches[1] + '"'));

function listTopNodes(node) {
  if (node.children) {
    node.children.forEach(c => {
      console.log(`${c.id}: ${c.name} (${c.type})`);
      if (c.children && c.name.includes('Template')) {
          c.children.forEach(gc => console.log(`  ${gc.id}: ${gc.name} (${gc.type})`));
      }
    });
  }
}

listTopNodes(data);
