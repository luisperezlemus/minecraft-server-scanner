"use client"
import React from "react"

import {useRouter} from "next/navigation"

const ServerCard = ({ server }) => {
    const router = useRouter()

    return (
        <div className="border p-3 rounded-lg shadow-md bg-white max-w-xs cursor-pointer hover:shadow-lg transition"
              onClick={() => router.push(`/server/${server.ip_address}:${server.port}`)}>
            {/* <h2 className="text-lg font-bold text-black">{server.ip_address}:{server.port}</h2> */}
            <h2 className="text-lg truncate font-bold text-black">{server.motd}</h2>
            <p className="text-sm text-black">IP: {server.ip_address}</p>
            <p className="text-sm text-black">Port: {server.port}</p>
            <p className="text-sm truncate text-black">Version: {server.version || "Unknown"}</p>
            <p className="text-sm text-black">Players: {server.players}</p>
            <p className="text-sm text-black">Gamemode: {server.gamemode || "N/A"}</p>
            {/* <p className="text-sm truncate text-black">MOTD: {server.motd || "No MOTD"}</p> */}
            {/* latency not needed  */}
            {/* <p className="text-sm text-black">Latency: {server.latency}ms</p> */}
            <p className="text-sm text-black">Country: {server.country_code || "Unknown"}</p>
            <p className="text-xs text-gray-800">Last Checked: {new Date(server.last_checked).toLocaleString()}</p>
        </div>
    )
}

export default ServerCard