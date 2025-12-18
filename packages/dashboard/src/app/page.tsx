import ChancellorView from "@/components/ChancellorView";

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white p-8 flex flex-col items-center justify-center relative overflow-hidden">
      {/* Background Grid Effect */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(20,20,20,0.5)_1px,transparent_1px),linear-gradient(90deg,rgba(20,20,20,0.5)_1px,transparent_1px)] bg-[size:40px_40px] pointer-events-none"></div>
      
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-green-900/10 blur-[100px] rounded-full pointer-events-none"></div>

      <div className="z-10 w-full max-w-5xl">
        <div className="mb-12 text-center space-y-2">
          <h1 className="text-4xl md:text-6xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-500">
            TRINITY DASHBOARD
          </h1>
          <p className="text-gray-500 font-mono text-sm tracking-widest uppercase">
            AFO Kingdom Operational Interface v1.0
          </p>
        </div>

        <ChancellorView />
      </div>
    </main>
  );
}
