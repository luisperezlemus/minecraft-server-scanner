import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import path from 'path';

const dbPath = path.resolve(process.cwd(), '../scanner/scan_db.db');
async function openDb() {
    return open({
        filename: dbPath,
        driver: sqlite3.Database
    })
}

export async function GET() {
    try {
        const db = await openDb();
        const serverCount = await db.get("SELECT COUNT(*) as count FROM online_servers")

        return Response.json({
            serverCount: serverCount.count
        })
    } catch (error) {
        return Response.json({ error: error.message }, { status: 500 })
    }
}