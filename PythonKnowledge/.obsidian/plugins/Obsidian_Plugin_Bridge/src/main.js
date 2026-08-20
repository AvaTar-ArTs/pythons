"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const obsidian_1 = require("obsidian");
const child_process_1 = require("child_process");
class PythonBridgePlugin extends obsidian_1.Plugin {
    async onload() {
        this.addCommand({
            id: 'run-python-bridge',
            name: 'Run Python Bridge Script',
            callback: () => {
                // Path to your bridge script
                const scriptPath = '/Users/steven/pythons/vault_bridge.py';
                (0, child_process_1.exec)(`python3 ${scriptPath}`, (error, stdout, stderr) => {
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
exports.default = PythonBridgePlugin;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoibWFpbi5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIm1haW4udHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7QUFBQSx1Q0FBa0M7QUFDbEMsaURBQXFDO0FBRXJDLE1BQXFCLGtCQUFtQixTQUFRLGlCQUFNO0lBQ3JELEtBQUssQ0FBQyxNQUFNO1FBQ1gsSUFBSSxDQUFDLFVBQVUsQ0FBQztZQUNmLEVBQUUsRUFBRSxtQkFBbUI7WUFDdkIsSUFBSSxFQUFFLDBCQUEwQjtZQUNoQyxRQUFRLEVBQUUsR0FBRyxFQUFFO2dCQUNkLDZCQUE2QjtnQkFDN0IsTUFBTSxVQUFVLEdBQUcsdUNBQXVDLENBQUM7Z0JBRTNELElBQUEsb0JBQUksRUFBQyxXQUFXLFVBQVUsRUFBRSxFQUFFLENBQUMsS0FBSyxFQUFFLE1BQU0sRUFBRSxNQUFNLEVBQUUsRUFBRTtvQkFDdkQsSUFBSSxLQUFLLEVBQUUsQ0FBQzt3QkFDWCxPQUFPLENBQUMsS0FBSyxDQUFDLFVBQVUsS0FBSyxDQUFDLE9BQU8sRUFBRSxDQUFDLENBQUM7d0JBQ3pDLE9BQU87b0JBQ1IsQ0FBQztvQkFDRCxPQUFPLENBQUMsR0FBRyxDQUFDLFdBQVcsTUFBTSxFQUFFLENBQUMsQ0FBQztnQkFDbEMsQ0FBQyxDQUFDLENBQUM7WUFDSixDQUFDO1NBQ0QsQ0FBQyxDQUFDO0lBQ0osQ0FBQztDQUNEO0FBbkJELHFDQW1CQyIsInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB7IFBsdWdpbiB9IGZyb20gJ29ic2lkaWFuJztcbmltcG9ydCB7IGV4ZWMgfSBmcm9tICdjaGlsZF9wcm9jZXNzJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgUHl0aG9uQnJpZGdlUGx1Z2luIGV4dGVuZHMgUGx1Z2luIHtcblx0YXN5bmMgb25sb2FkKCkge1xuXHRcdHRoaXMuYWRkQ29tbWFuZCh7XG5cdFx0XHRpZDogJ3J1bi1weXRob24tYnJpZGdlJyxcblx0XHRcdG5hbWU6ICdSdW4gUHl0aG9uIEJyaWRnZSBTY3JpcHQnLFxuXHRcdFx0Y2FsbGJhY2s6ICgpID0+IHtcblx0XHRcdFx0Ly8gUGF0aCB0byB5b3VyIGJyaWRnZSBzY3JpcHRcblx0XHRcdFx0Y29uc3Qgc2NyaXB0UGF0aCA9ICcvVXNlcnMvc3RldmVuL3B5dGhvbnMvdmF1bHRfYnJpZGdlLnB5Jztcblx0XHRcdFx0XG5cdFx0XHRcdGV4ZWMoYHB5dGhvbjMgJHtzY3JpcHRQYXRofWAsIChlcnJvciwgc3Rkb3V0LCBzdGRlcnIpID0+IHtcblx0XHRcdFx0XHRpZiAoZXJyb3IpIHtcblx0XHRcdFx0XHRcdGNvbnNvbGUuZXJyb3IoYEVycm9yOiAke2Vycm9yLm1lc3NhZ2V9YCk7XG5cdFx0XHRcdFx0XHRyZXR1cm47XG5cdFx0XHRcdFx0fVxuXHRcdFx0XHRcdGNvbnNvbGUubG9nKGBPdXRwdXQ6ICR7c3Rkb3V0fWApO1xuXHRcdFx0XHR9KTtcblx0XHRcdH1cblx0XHR9KTtcblx0fVxufVxuIl19