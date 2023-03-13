const fs = require('fs');

const readline = () => {
	try {
		const data = fs.readFileSync('./input.txt', 'utf8').split("\n");
		const ret = data[0]
		fs.writeFileSync('./input.txt', data.splice(1).join("\n"))
		return ret
	} catch (err) {
		console.error(err);
		return "";
	}
}

module.exports = readline