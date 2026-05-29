const fs = require('fs');
const path = require('path');

// Read the inspection output from the tool output file
const outputFilePath = process.argv[2];
const content = fs.readFileSync(outputFilePath, 'utf8');

// The output contains JSON messages. We need to find the one with the result.
const matches = content.match(/\{"jsonrpc":"2.0","id":2,"result":\{"content":\[\{"type":"text","text":"(.*?)"\}\],"isError":false\}\}/);

if (!matches) {
  console.error('Could not find the result JSON');
  process.exit(1);
}

const escapedJson = matches[1];
const jsonStr = JSON.parse('"' + escapedJson + '"'); // Unescape
const data = JSON.parse(jsonStr);

function findSections(node, results = {}) {
  if (node.name && node.name.includes('SLIDE')) {
    results[node.name] = node.id;
  }
  if (node.children) {
    node.children.forEach(c => findSections(c, results));
  }
  return results;
}

const sections = findSections(data);
console.log(JSON.stringify(sections, null, 2));
