import sqlite3 from 'sqlite3';
import {open} from "sqlite"
import path from "path"

const dbPath = path.resolve(process.cwd(), '../scanner/scan_db.db');
async function openDb() {
    return open({
        filename: dbPath,
        driver: sqlite3.Database
    })
}

export async function GET(req, {params}) {
    const {ip_port} = await params
    const ip_address = ip_port.split(":")[0]
    const port = ip_port.split(":")[1]

    try {
        const db = await openDb();
        const serverDetails = await db.all("SELECT * FROM online_servers WHERE ip_address = ? AND port = ?", [ip_address, port])

        return Response.json({
            server: serverDetails[0]
        })
    } catch (error) {
        return Response.json({ error: error.message }, { status: 500 })
    }
}