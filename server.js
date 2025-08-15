import express from "express";
import bodyParser from "body-parser";
import cors from "cors";
import fs from "fs";
import { logActivity } from "./logger.js";

const app = express();
app.use(cors());
app.use(bodyParser.json());
app.use(express.static("public"));

// Log activity route
app.post("/log", (req, res) => {
    const { user, action } = req.body;
    logActivity(user, action);
    res.json({ success: true });
});

// Get all logs
app.get("/logs", (req, res) => {
    const logs = fs.existsSync("./logs.json")
        ? JSON.parse(fs.readFileSync("./logs.json", "utf-8"))
        : [];
    res.json(logs);
});

app.listen(4000, () => {
    console.log("Server running at http://localhost:4000");
});