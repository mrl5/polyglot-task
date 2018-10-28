#!/usr/bin/env node

if (process.argv.length > 2) {
    let expressions = process.argv.slice(2);
    expressions.forEach((expression) => {
        console.log(expression);
    });
} else {
    console.error("API error: expected at least one argument");
    process.exit(1);
}
