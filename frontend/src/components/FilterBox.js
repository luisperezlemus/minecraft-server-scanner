"use client"

import { useState, useEffect} from "react"

import CountryDropDown from "./CountryDropDown"

const FilterBox = ({port, setPort, version, setVersion, country, setCountry}) => {

    const [hasInteracted, setHasInteracted] = useState([false, false, false])

    useEffect(() => {
        const savedPort = sessionStorage.getItem("port") || ""
        const savedVersion = sessionStorage.getItem("version") || ""
        const savedCountry = sessionStorage.getItem("country") || ""

        setPort(savedPort)
        setVersion(savedVersion)
        setCountry(savedCountry)
        
        setHasInteracted([
            savedPort !== "",
            savedVersion !== "",
            savedCountry !== ""
        ])

    }, [])

    const handleFilterChange = (index, key, setFilter) => (e) => 
        {
            console.log(key, ": ", e.target.value)
            setFilter(e.target.value)
            sessionStorage.setItem(key, e.target.value)

            setHasInteracted((prev) => {
                const newState = [...prev]
                newState[index] = true
                return newState
            })
            // console.log(e.target.value)
        }

    return (
        // Filter Box
        <div className="flex justify-center gap-4 mb-6">
            {/* Port (Java or Bedrock) */}
            <p>Edition:</p>
            <select className={`p-2 border rounded text-black transition-opacity duration-300 ${hasInteracted[0] ? "opacity-100" : "opacity-50"}`}
              value={port} onChange={handleFilterChange(0, "port", setPort)}>
                <option value="">All</option>
                <hr />
                <option value="25565">Java</option>
                <option value="19132">Bedrock</option>
            </select>

            {/* Version */}
            <p>Version:</p>
            <select className={`p-2 border rounded text-black transition-opacity duration-300 ${hasInteracted[1] ? "opacity-100" : "opacity-50"}`} 
              value={version} onChange={handleFilterChange(1, "version", setVersion)}>
                <option value="">All</option>
                <hr />
                <option value="1.0">1.0</option>
                <option value="1.2">1.2</option>
                <option value="1.3">1.3</option>
                <option value="1.4">1.4</option>
                <option value="1.5">1.5</option>
                <option value="1.6">1.6</option>
                <option value="1.7">1.7</option>
                <option value="1.8">1.8</option>
                <option value="1.9">1.9</option>
                <option value="1.10">1.10</option>
                <option value="1.11">1.11</option>
                <option value="1.12">1.12</option>
                <option value="1.13">1.13</option>
                <option value="1.14">1.14</option>
                <option value="1.15">1.15</option>
                <option value="1.16">1.16</option>
                <option value="1.17">1.17</option>
                <option value="1.18">1.18</option>
                <option value="1.19">1.19</option>
                <option value="1.20">1.20</option>
                <option value="1.21">1.21</option>
            </select>
            {/* Country */}
            <p>Country:</p>
            <CountryDropDown country={country}  hasInteracted={hasInteracted[2]} onChange={handleFilterChange(2, "country", setCountry)}/>
        </div>
    )
}

export default FilterBox