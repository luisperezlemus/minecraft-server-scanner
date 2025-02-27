import ServerList from "../components/ServerList"

export default async function Home() {
  return (
    <main className="container mx-auto p-4">
      <h1 className="text-center text-3xl font-bold">Minecraft Servers Online</h1>
      <ServerList />
    </main>
  )
}