const prompt = require('prompt-sync') ({sigint: true});

readlinetest = () => {
	let line = prompt('');
	return line
}

module.exports = readlinetest

