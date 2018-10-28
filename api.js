#!/usr/bin/env node
var spawn = require('child_process').spawn;

function callWorker(argument, id) {
    let processStart = new Date();
    let workerCmd = "./worker.py";
    let worker = spawn(workerCmd, [argument]);
    worker.stdout.on('data', (data) => {
        elapsedTime = new Date() - processStart;
        console.log(`${id}: ${data.toString().trim()}, ${elapsedTime/1000}`);
    });
    worker.stderr.on('data', (data) => {
        elapsedTime = new Date() - processStart;
        console.error(`${id}: error, ${elapsedTime/1000}`);
    });
}

if (process.argv.length > 2) {
    let expressions = process.argv.slice(2);
    expressions.forEach((expression, index) => {
        console.log(`${index}: ${expression}`);
        callWorker(expression, index);
    });
} else {
    console.error("API error: expected at least one argument");
    process.exit(1);
}
