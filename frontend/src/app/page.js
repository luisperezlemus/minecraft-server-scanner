"use client"

import {useState, useEffect} from "react"

import ServerList from "../components/ServerList"
import FilterBox from "../components/FilterBox"

export default function Home() {
  const [port, setPort] = useState("")
  const [version, setVersion] = useState("")
  const [country, setCountry] = useState("")


  return (
    <main className="container mx-auto p-4">
      <h1 className="text-center text-3xl font-bold">Minecraft Servers Online</h1>
      <FilterBox port={port} setPort={setPort} version={version} setVersion={setVersion} country={country} setCountry={setCountry}/>
      <ServerList port={port} version={version} country={country}/>
    </main>
  )
}