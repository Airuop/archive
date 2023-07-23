const fs = require('fs');
const Worker = fs.readFileSync('./output.txt',
    { encoding: 'utf8', flag: 'r' });

const num1 = 10;
const num2 = 2230;

const sum = num1 + num2;

console.log(`The sum is: ${sum} az qabl ${Worker} l`);
