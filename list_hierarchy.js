const fs = require('fs');

const content = fs.readFileSync(process.argv[2], 'utf8');
const startTag = '"text":"';
const endTag = '"}]},"isError"';

const startIdx = content.indexOf(startTag);
if (startIdx === -1) {
    console.error('Start tag not found');
    process.exit(1);
}

const endIdx = content.indexOf(endTag, startIdx);
if (endIdx === -1) {
    console.error('End tag not found');
    process.exit(1);
}

let jsonStr = content.substring(startIdx + startTag.length, endIdx);
// Unescape the string
jsonStr = jsonStr.replace(/\\"/g, '"').replace(/\\\\/g, '\\');

const data = JSON.parse(jsonStr);

function printNodes(node, indent = '') {
    console.log(`${indent}${node.id}: ${node.name} (${node.type})`);
    if (node.children) {
        node.children.forEach(c => printNodes(c, indent + '  '));
    }
}

printNodes(data);
