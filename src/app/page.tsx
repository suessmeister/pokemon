'use client'

import Image from 'next/image'
import { useState } from 'react'
import { WalletButton } from '@/components/solana/solana-provider'
import { useWallet } from '@solana/wallet-adapter-react'
import pokemonData from '@/data/pokemon.json'

export default function Home() {
  const [imageError, setImageError] = useState<{ [key: string]: boolean }>({})
  const { publicKey } = useWallet()

  return (
    <main className="min-h-screen p-8 bg-gradient-to-b from-blue-500 to-blue-700">
      <div className="max-w-6xl mx-auto">
        {/* Header with wallet */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-yellow-300 pokemon-title">
            Possible NFTs:
          </h1>
          <WalletButton className="btn btn-primary" />
        </div>

        {/* Wallet status message */}
        {!publicKey && (
          <div className="text-center mb-8 p-4 bg-yellow-400/20 rounded-lg">
            <p className="text-yellow-300 text-lg">
              Connect your wallet to start collecting Pokemon NFTs!
            </p>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {pokemonData.pokemon.map((poke) => (
            <div
              key={poke.name}
              className={`rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-200 type-${poke.type}`}
            >
              <div className="relative h-64 bg-white/90">
                {!imageError[poke.name] ? (
                  <Image
                    src={`/mons/${poke.name}_nft.png`}
                    alt={poke.name}
                    fill
                    style={{ objectFit: 'contain' }}
                    className="p-4"
                    onError={() => setImageError(prev => ({ ...prev, [poke.name]: true }))}
                    priority
                  />
                ) : (
                  <div className="flex items-center justify-center h-full text-gray-500">
                    <p>Image not available</p>
                  </div>
                )}
              </div>
              <div className="p-4 bg-white">
                <h2 className="text-2xl font-bold text-center">{poke.name}</h2>
                <div className="flex justify-between mt-2">
                  <span className="text-gray-600">Type: {poke.type}</span>
                  <span className="text-red-500">HP: {poke.hp}</span>
                </div>
                {/* Show attacks when wallet is connected */}
                {publicKey && (
                  <div className="mt-2 space-y-1">
                    {poke.attacks.map((attack, index) => (
                      <div key={index} className="flex justify-between text-sm">
                        <span className="text-gray-700">{attack.name}</span>
                        <span className="text-blue-600">{attack.damage} DMG</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Debug info - only show if wallet is connected */}
        {publicKey && (
          <div className="mt-8 p-4 bg-white/10 rounded-lg text-white">
            <h2 className="text-xl font-bold mb-2">Image Loading Debug Info:</h2>
            <p>Make sure your NFT images are in the following path:</p>
            <code className="block bg-black/30 p-2 rounded mt-1">
              public/mons/[PokemonName]_nft.png
            </code>
            <p className="mt-2">Expected files:</p>
            <ul className="list-disc list-inside">
              {pokemonData.pokemon.map(poke => (
                <li key={poke.name} className={imageError[poke.name] ? 'text-red-300' : 'text-green-300'}>
                  {`/mons/${poke.name}_nft.png`} - {imageError[poke.name] ? 'Not found' : 'OK'}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </main>
  )
}
