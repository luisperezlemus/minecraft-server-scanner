import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import path from 'path';

// Eventually will use postgresql
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

    const port = url.searchParams.get('port')
    const version = url.searchParams.get('version')
    const country = url.searchParams.get('country')

    try {
        const db = await openDb();
        let query = "SELECT * FROM online_servers WHERE 1=1"
        let countQuery = "SELECT COUNT(*) as count FROM online_servers WHERE 1=1"
        let params = []
        let countParams = []

        // conditional because not all arguments are passed
        if (port) { 
            query += " AND port = ?"
            countQuery += " AND port = ?"
            params.push(port)
            countParams.push(port)
        }

        if (version) {
            query += " AND version LIKE ?"
            countQuery += " AND version LIKE ?"
            params.push(version + ".%")
            countParams.push(version + ".%")
        }

        if (country) {
            query += " AND country_code = ?"
            countQuery += " AND country_code = ?"
            params.push(country)
            countParams.push(country)
        }

        query += " ORDER BY last_checked DESC LIMIT ? OFFSET ?" // ordered by most recent
        params.push(limit, offset)

        const online_servers = await db.all(query, params)
        const total = await db.get(countQuery, countParams)
        
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