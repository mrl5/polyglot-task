#!/usr/bin/env node
var startTime = new Date();
var spawn = require('child_process').spawn;
var result = new Map();
var api = require('commander');

/* flags */
api
  .version('1.0.0-SNAPSHOT')
  .option('-u, --uuid', "Universally Unique IDentifier of the endpoint request")
  .description("API for getting requests, sending to the worker and logging (requests, inputs, errors)")
  .parse(process.argv);

function callWorker(argument, id, noOfArgs) {
    let processStart = new Date();
    let workerCmd = "./worker.py";
    let worker = spawn(workerCmd, [argument]);
    worker.stdout.on('data', (data) => {
        elapsedTime = new Date() - processStart;
        result.set(id, [data.toString().trim(), elapsedTime / 1000]);
    });
    worker.stderr.on('data', (data) => {
        elapsedTime = new Date() - processStart;
        result.set(id, ["error", elapsedTime / 1000]);
        //logError();
    });
    worker.on('close', (code) => {
        /* add exit code */
        let tmpArray = result.get(id);
        tmpArray.push(code);
        result.set(id, tmpArray);

        if (id + 1 === noOfArgs) {
            printOutput();
            getTotalTime();
        }
    });
}

function printOutput() {
    let item;
    for (let i = 0; i < result.size; i++) {
        item = result.get(i);
        /* STDOUT if exit code was 0 */
        if (item[2] === 0) {
            console.log(`${item[0]}, ${item[1]}`);
        } else {
            console.error(`${item[0]}, ${item[1]}`);
        }
    }
}

function getTotalTime() {
    let totalTime = new Date() - startTime;
    console.log(`total time: ${totalTime / 1000}`);
}

function main() {
    if (api.args.length > 0) {
        //logRequest(uuid);
        api.args.forEach((expression, index) => {
            //logInput(expression);
            callWorker(expression, index, api.args.length);
        });
    } else {
        console.error("API error: expected at least one argument");
        process.exit(1);
    }
}

main();
