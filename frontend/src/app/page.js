import ServerList from "../components/ServerList"
import FilterBox from "../components/FilterBox"
export default async function Home() {

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-center text-3xl font-bold">Minecraft Servers Online</h1>
      <FilterBox />
      <ServerList />
    </main>
  )
}