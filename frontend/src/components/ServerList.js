"use client"

import {useEffect, useState} from "react"
import ServerCard from "./ServerCard"

const ServerList = () => {
    const [servers, setServers] = useState([])
    const [page, setPage] = useState(1)
    const [totalPages, setTotalPages] = useState(1)
    const [loading, setLoading] = useState(true)
    const [serverCount, setServerCount] = useState(0)
    const [limit, setLimit] = useState(null)

    // Determine the number of servers to display per page, based on screen size
    useEffect(() => {
        const updateLimit = () => {
            const height = window.innerHeight
            const width = window.innerWidth

            let newLimit

            if (width >= 1280) { // large screens
                newLimit = Math.floor((height - 200) / 180) * 5
            }
            else if (width >= 1024) { 
                newLimit = Math.floor((height - 200) / 180) * 4
            }
            else if (width >= 768) { 
                newLimit = Math.floor((height - 200) / 180) * 3
            }
            else { // small screens
                newLimit = Math.floor((height - 200) / 180)
            }

            setLimit(newLimit)
        }

        updateLimit()
        window.addEventListener('resize', updateLimit)

        return () => window.removeEventListener('resize', updateLimit)
    }, [])

    // this only runs once to fetch the server count
    useEffect(() => {
        async function fetchServerCount() {
            const res = await fetch('/api/serverCount')
            const data = await res.json()
            setServerCount(data.serverCount)
        }
        fetchServerCount()
    }, [])

    useEffect(() => {
        if (limit === null) return
        const fetchServers = async () => {
            try {
                const response = await fetch(`/api/servers?page=${page}&limit=${limit}`)
                const data = await response.json()
                setServers(data.online_servers)
                setTotalPages(data.totalPages)
            } 
            catch (error) {
                console.error(error)
            }
            finally {
                setLoading(false)
            }
        }
        fetchServers()
    }, [page, limit])

    if (loading) return <p>Fetching Servers...</p>

    return (
        <div className="p-4 flex flex-col items-center">
            <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
                {servers.map((server, index) => (
                    <ServerCard key={index} server={server} />
                ))}
            </div>

            <div className="flex justify-center mt-4 space-x-4">
                <button className="px-4 py-2 bg-blue-500 rounded disabled:opacity-50"
                    onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
                    disabled={page === 1}
                >
                    Previous
                </button>
                <span className="px-4 py-2 text-white">{page} / {totalPages}</span>
                <button className="px-4 py-2 bg-blue-500 rounded disabled:opacity-50"
                    onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
                    disabled={page === totalPages}
                >
                    Next
                </button> 
            </div>
            <br />
            <p className="text-center text-lg">Tracking {serverCount} servers</p>
        </div>
    )
}

export default ServerList