#!/usr/bin/env node
var startTime = new Date();
var spawn = require('child_process').spawn;

function callWorker(argument, id, noOfArgs) {
    let processStart = new Date();
    let workerCmd = "./worker.py";
    let worker = spawn(workerCmd, [argument]);
    worker.stdout.on('data', (data) => {
        elapsedTime = new Date() - processStart;
        console.log(`${id}: ${data.toString().trim()}, ${elapsedTime / 1000}`);
    });
    worker.stderr.on('data', (data) => {
        elapsedTime = new Date() - processStart;
        console.error(`${id}: error, ${elapsedTime / 1000}`);
    });
    worker.on('close', () => {
        if (id + 1 === noOfArgs) {
            getTotalTime();
        }
    });
}

function getTotalTime() {
    let totalTime = new Date() - startTime;
    console.log(`total time: ${totalTime / 1000}`);
}

if (process.argv.length > 2) {
    let expressions = process.argv.slice(2);
    expressions.forEach((expression, index) => {
        console.log(`${index}: ${expression}`);
        callWorker(expression, index, expressions.length);
    });
} else {
    console.error("API error: expected at least one argument");
    process.exit(1);
}
