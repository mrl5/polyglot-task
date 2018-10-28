#!/usr/bin/env node
var spawn = require('child_process').spawn;

function callWorker(argument) {
    let id = Symbol(argument);
    console.time(id.toString());
    let workerCmd = "./worker.py";
    let worker = spawn(workerCmd, [argument]);
    worker.stdout.on('data', (data) => {
        console.log(`${argument}: ${data.toString()}`);
    });
    worker.stderr.on('data', (data) => {
        console.error(`${argument}: error`);
    });
    worker.on('close', () => {
        console.timeEnd(id.toString());
    });

}

if (process.argv.length > 2) {
    let expressions = process.argv.slice(2);
    expressions.forEach((expression) => {
        callWorker(expression);
    });
} else {
    console.error("API error: expected at least one argument");
    process.exit(1);
}
