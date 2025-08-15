import fs from "fs";
const logFile = "./logs.json";

export function logActivity(user, action) {
    const logs = fs.existsSync(logFile)
        ? JSON.parse(fs.readFileSync(logFile, "utf-8"))
        : [];
    logs.push({ user, action, timestamp: new Date() });
    fs.writeFileSync(logFile, JSON.stringify(logs, null, 2));
}