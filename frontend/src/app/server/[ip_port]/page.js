"use client"

import {use, useEffect, useState} from "react"
import {useParams} from "next/navigation"

const ServerPage = () => {
    const {ip_port} = useParams()
    // : is encoded by %3A so we will separate using that as the delimiter
    const [server, setServer] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchServer = async () => {
            try {
                const res = await fetch(`/api/servers/${ip_port}`)
                const data = await res.json()
                setServer(data.server)
            }
            catch (error) {
                console.log(error)
            }
            finally {
                setLoading(false)
            }
        }
        fetchServer()
    }, [ip_port])

    if (loading) return <p>Loading...</p>
    if (!server) return <p>Server not found</p>


    return (
        <div className="p-6 max-w-3xl mx-auto">
            <h1 className="text-2xl font-bold">{server.motd}</h1>
            <p className="text-gray-300">IP: {server.ip_address}</p>
            <p className="text-gray-300">Port: {server.port}</p>
            <p className="text-gray-300">Version: {server.version}</p>
            <p className="text-gray-300">Players: {server.players}</p>
            <p className="text-gray-300">Gamemode: {server.gamemode || "N/A"}</p>
            <p className="text-gray-300">Country: {server.country_code}</p>
            <p className="text-gray-300">Latency: {server.latency ? server.latency + "ms" : "N/A"}</p>
            <p className="text-gray-300">Last Checked: {new Date(server.last_checked).toLocaleString()}</p>
        </div>
    )
}

export default ServerPage