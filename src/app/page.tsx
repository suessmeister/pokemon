'use client'

import { useRouter } from 'next/navigation'
import { WalletButton } from '@/components/solana/solana-provider'
import { useWallet } from '@solana/wallet-adapter-react'
import Image from 'next/image'

export default function Home() {
  const router = useRouter()
  const { publicKey } = useWallet()

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-blue-500 to-blue-700 p-8 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-0 left-0 w-64 h-64 bg-yellow-300/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-0 right-0 w-64 h-64 bg-red-300/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
      </div>

      {/* Pokemon Fan Display */}
      <div className="relative w-full max-w-4xl h-[500px] mb-16">
        {/* Charizard - Left */}
        <div className="absolute left-[15%] top-1/2 -translate-y-1/2 transform -rotate-15 -skew-y-3 z-20 hover:scale-105 transition-transform duration-300">
          <div className="relative w-64 h-96">
            <Image
              src="/mons/Charizard_nft.png"
              alt="Charizard"
              fill
              style={{ objectFit: 'contain' }}
              className="drop-shadow-2xl"
              priority
            />
          </div>
        </div>

        {/* Blastoise - Center */}
        <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 transform z-30 hover:scale-105 transition-transform duration-300">
          <div className="relative w-64 h-96">
            <Image
              src="/mons/Blastoise_nft.png"
              alt="Blastoise"
              fill
              style={{ objectFit: 'contain' }}
              className="drop-shadow-2xl"
              priority
            />
          </div>
        </div>

        {/* Venusaur - Right */}
        <div className="absolute right-[15%] top-1/2 -translate-y-1/2 transform rotate-15 skew-y-3 z-20 hover:scale-105 transition-transform duration-300">
          <div className="relative w-64 h-96">
            <Image
              src="/mons/Venusaur_nft.png"
              alt="Venusaur"
              fill
              style={{ objectFit: 'contain' }}
              className="drop-shadow-2xl"
              priority
            />
          </div>
        </div>
      </div>

      <div className="text-center max-w-2xl relative z-10 -mt-16">
        <h1 className="text-7xl font-bold text-yellow-300 mb-6 pokemon-title">
          Mint. Upgrade. Earn.
        </h1>

        <div className="bg-black/30 backdrop-blur-sm rounded-xl p-6 mb-8 border border-yellow-300/30">
          <p className="text-white text-xl mb-4">
            ***WE ARE NOT ENDORSED OR SPONSORED BY NINTENDO***
          </p>
          <div className="space-y-2 text-left">
            <p className="text-white text-lg flex items-center">
              <span className="w-6 h-6 bg-yellow-300 text-black rounded-full flex items-center justify-center mr-2">1</span>
              Open 2 free packs/day or more, if you wish
            </p>
            <p className="text-white text-lg flex items-center">
              <span className="w-6 h-6 bg-yellow-300 text-black rounded-full flex items-center justify-center mr-2">2</span>
              Use them in battles
            </p>
            <p className="text-white text-lg flex items-center">
              <span className="w-6 h-6 bg-yellow-300 text-black rounded-full flex items-center justify-center mr-2">3</span>
              Be careful not to let your mons catch STDs...
            </p>
            <p className="text-white text-lg flex items-center">
              <span className="w-6 h-6 bg-yellow-300 text-black rounded-full flex items-center justify-center mr-2">4</span>
              Climb the leaderboards for shiny packs
            </p>
          </div>
        </div>

        {publicKey ? (
          <button
            onClick={() => router.push('/collection')}
            className="px-8 py-4 bg-yellow-300 text-black font-bold rounded-lg hover:bg-yellow-400 transition-colors text-xl transform hover:scale-105 transition-transform duration-300 shadow-lg hover:shadow-yellow-300/50"
          >
            Let's Go {'-->'}
          </button>
        ) : (
          <div className="flex flex-col items-center gap-4">
            <p className="text-white text-lg">
              Connect your wallet to start collecting!
            </p>
            <WalletButton className="px-8 py-4 bg-yellow-300 text-black font-bold rounded-lg hover:bg-yellow-400 transition-colors text-xl transform hover:scale-105 transition-transform duration-300 shadow-lg hover:shadow-yellow-300/50" />
          </div>
        )}
      </div>
    </main>
  )
}
