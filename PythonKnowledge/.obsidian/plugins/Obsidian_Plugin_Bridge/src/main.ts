import { Plugin } from 'obsidian';
import { exec } from 'child_process';

export default class PythonBridgePlugin extends Plugin {
	async onload() {
		this.addCommand({
			id: 'run-python-bridge',
			name: 'Run Python Bridge Script',
			callback: () => {
				// Path to your bridge script
				const scriptPath = '/Users/steven/pythons/vault_bridge.py';
				
				exec(`python3 ${scriptPath}`, (error, stdout, stderr) => {
					if (error) {
						console.error(`Error: ${error.message}`);
						return;
					}
					console.log(`Output: ${stdout}`);
				});
			}
		});
	}
}
