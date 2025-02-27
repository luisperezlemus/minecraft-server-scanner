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

export async function GET(req) {
    const url = new URL(req.url)
    const page = parseInt(url.searchParams.get('page') || "1", 10)
    const limit = parseInt(url.searchParams.get('limit') || "10", 10)
    const offset = (page - 1) * limit

    try {
        const db = await openDb();
        const online_servers = await db.all("SELECT * FROM online_servers ORDER BY last_checked DESC LIMIT ? OFFSET ?", [limit, offset])
        
        const total = await db.get("SELECT COUNT(*) as count FROM online_servers")

        return Response.json({
            online_servers,
            total: total.count,
            page,
            totalPages: Math.ceil(total.count / limit)
        })
    } catch (error) {
        return Response.json({ error: error.message }, { status: 500 })
    }
}