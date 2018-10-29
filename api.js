#!/usr/bin/env node
var startTime = new Date();
var spawn = require('child_process').spawn;
var result = new Map();
var api = require('commander');

/* flags */
api
  .version('1.0.0-SNAPSHOT')
  .option('-u, --uuid [type]', "Universally Unique IDentifier of the endpoint request")
  .description("API for getting requests, sending to the worker and logging (requests, inputs, errors)")
  .parse(process.argv);

function callWorker(argument, id, noOfArgs) {
    let processStart = new Date();
    let workerCmd = "./worker.py";
    let worker = spawn(workerCmd, [argument]);
    worker.stdout.on('data', (data) => {
        result.set(id, [data.toString().trim(), getDuration(processStart) / 1000]);
    });
    worker.stderr.on('data', (data) => {
        result.set(id, ["error", getDuration(processStart) / 1000]);
        //logError();
    });
    worker.on('close', (code) => {
        /* add exit code */
        let tmpArray = result.get(id);
        tmpArray.push(code);
        result.set(id, tmpArray);

        if (id + 1 === noOfArgs) {
            printOutput(result);
            console.log(`total time: ${getDuration(startTime) / 1000}`);
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
