#!/usr/bin/env node
var startTime = new Date();
var spawn = require('child_process').spawn;
var result = new Map();

/* flags */
var api = require('commander');
api
  .version('1.0.0-SNAPSHOT')
  .option('-u, --uuid [type]', "Universally Unique IDentifier of the endpoint request", 'internal')
  .description("API for getting requests, sending to the worker and logging (requests, inputs, errors)")
  .parse(process.argv);

function callWorker(argument, id, noOfArgs) {
    let processStart = new Date();
    let elapsedTime;
    let workerCmd = "./worker.py";
    let worker = spawn(workerCmd, [argument]);
    worker.stdout.on('data', (data) => {
        elapsedTime = getDuration(processStart) / 1000;
        result.set(id, [data.toString().trim(), elapsedTime]);
    });
    worker.stderr.on('data', (data) => {
        elapsedTime = getDuration(processStart) / 1000;
        result.set(id, ["error", elapsedTime]);
        //logError();
    });
    worker.on('close', (code) => {
        /* add exit code */
        let tmpArray = result.get(id);
        tmpArray.push(code);
        result.set(id, tmpArray);
        logInput(api.uuid, argument, elapsedTime);

        if (id + 1 === noOfArgs) {
            printOutput(result);
            const totalTime = getDuration(startTime) / 1000;
            logRequest(api.uuid, totalTime, noOfArgs);
        }
    });
}

function printOutput(resultArray) {
    let item;
    for (let i = 0; i < resultArray.size; i++) {
        item = resultArray.get(i);
        /* STDOUT if exit code was 0 */
        if (item[2] === 0) {
            console.log(`${item[0]}, ${item[1]}`);
        } else {
            console.error(`${item[0]}, ${item[1]}`);
        }
    }
}

function getDuration(startTime) {
    let duration = new Date() - startTime;
    return duration;
}

function logRequest(uuid, elapsedTime, noOfExpressions) {
    console.log(`[${new Date().toISOString()}]\t${uuid}\t${elapsedTime}\t${noOfExpressions}`);
}

function logInput(uuid, input, elapsedTime) {
    console.log(`${uuid}\t${elapsedTime}\t${input}`)
}

function main() {
    if (api.args.length > 0) {
        api.args.forEach((expression, index) => {
            callWorker(expression, index, api.args.length);
        });
    } else {
        console.error("API error: expected at least one argument");
        process.exit(1);
    }
}

main();
