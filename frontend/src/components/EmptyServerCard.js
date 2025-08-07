"use client"
import React from "react"

const EmptyServerCard = () => {
    return (
        <div className="animate-pulse border p-3 rounded-lg shadow-md bg-white w-full">
            <div className="h-6 bg-gray-200 rounded mb-2 w-full"/>
            <div className="h-4 bg-gray-200 rounded mb-1 w-1/2"/>
            <div className="h-4 bg-gray-200 rounded mb-1 w-1/3"></div>    {/* Port */}
            <div className="h-4 bg-gray-200 rounded mb-1 w-1/2"></div>    {/* Version */}
            <div className="h-4 bg-gray-200 rounded mb-1 w-1/3"></div>    {/* Players */}
            <div className="h-4 bg-gray-200 rounded mb-1 w-1/2"></div>    {/* Gamemode */}
            <div className="h-4 bg-gray-200 rounded mb-1 w-1/3"></div>    {/* Country */}
            <div className="h-3 bg-gray-200 rounded w-4/5"></div>         {/* Last Checked */}
        </div>
    )
}

export default EmptyServerCard