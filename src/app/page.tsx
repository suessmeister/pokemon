'use client'

import Image from 'next/image'
import { useState } from 'react'
import { WalletButton } from '@/components/solana/solana-provider'
import { useWallet } from '@solana/wallet-adapter-react'
import pokemonData from '@/data/pokemon.json'
import shiningData from '@/data/shining.json'

export default function Home() {
  const [imageError, setImageError] = useState<{ [key: string]: boolean }>({})
  const [activeTab, setActiveTab] = useState<'available' | 'owned'>('available')
  const { publicKey, disconnect } = useWallet()

  return (
    <main className="min-h-screen p-8 bg-gradient-to-b from-blue-500 to-blue-700">
      <div className="max-w-6xl mx-auto">
        {/* Header with wallet */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-yellow-300 pokemon-title">
            Pokemon NFTs
          </h1>
          {publicKey ? (
            <div className="flex items-center gap-2">
              <button
                onClick={disconnect}
                className="btn !bg-white !text-black hover:!bg-gray-100"
              >
                Disconnect?
              </button>

            </div>
          ) : (
            <WalletButton className="btn btn-primary" />
          )}
        </div>

        {/* Wallet status message */}
        {!publicKey && (
          <div className="text-center mb-8 p-4 bg-yellow-400/20 rounded-lg">
            <p className="text-yellow-300 text-lg">
              Connect your wallet to start collecting Pokemon NFTs!
            </p>
          </div>
        )}

        {/* Tab Navigation */}
        {publicKey && (
          <div className="flex justify-center mb-8">
            <div className="bg-black/20 rounded-lg p-1">
              <button
                onClick={() => setActiveTab('available')}
                className={`px-6 py-2 rounded-md transition-colors ${activeTab === 'available'
                  ? 'bg-yellow-300 text-black'
                  : 'text-white hover:bg-black/30'
                  }`}
              >
                Available Pokemon
              </button>
              <button
                onClick={() => setActiveTab('owned')}
                className={`px-6 py-2 rounded-md transition-colors ${activeTab === 'owned'
                  ? 'bg-yellow-300 text-black'
                  : 'text-white hover:bg-black/30'
                  }`}
              >
                My Pokemon
              </button>
            </div>
          </div>
        )}

        {/* Available Pokemon Section */}
        {activeTab === 'available' && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {pokemonData.pokemon.map((poke) => (
                <div
                  key={poke.name}
                  className="transform hover:scale-105 transition-transform duration-200"
                >
                  <div className="relative h-[500px]">
                    {!imageError[poke.name] ? (
                      <Image
                        src={`/mons/${poke.name}_nft.png`}
                        alt={poke.name}
                        fill
                        style={{ objectFit: 'contain' }}
                        className="p-2"
                        onError={() => setImageError(prev => ({ ...prev, [poke.name]: true }))}
                        priority
                      />
                    ) : (
                      <div className="flex items-center justify-center h-full text-gray-500">
                        <p>Image not available</p>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Shining Pokemon Section */}
            <div className="mt-16">
              <h1 className="text-5xl font-bold text-yellow-300 pokemon-title mb-8 text-center">
                Shining Pokemon
              </h1>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {shiningData.shining.map((poke) => (
                  <div
                    key={`shiny-${poke.name}`}
                    className="transform hover:scale-105 transition-transform duration-200"
                  >
                    <div className="relative h-[500px]">
                      {!imageError[`shiny-${poke.name}`] ? (
                        <Image
                          src={`/mons/shiny/${poke.name}_nft.png`}
                          alt={`Shining ${poke.name}`}
                          fill
                          style={{ objectFit: 'contain' }}
                          className="p-2"
                          onError={() => setImageError(prev => ({ ...prev, [`shiny-${poke.name}`]: true }))}
                          priority
                        />
                      ) : (
                        <div className="flex items-center justify-center h-full text-gray-300">
                          <p>Image not available</p>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}

        {/* Owned Pokemon Section */}
        {activeTab === 'owned' && publicKey && (
          <div className="text-center">
            <div className="bg-black/20 rounded-lg p-8">
              <h2 className="text-2xl font-bold text-yellow-300 mb-4">Your Pokemon Collection</h2>
              <p className="text-white mb-2">Showing Pokemon for wallet:</p>
              <p className="text-yellow-300 font-mono text-sm mb-4 break-all">{publicKey.toString()}</p>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {/* Placeholder for owned Pokemon - will be populated with actual data */}
                <div className="bg-black/30 rounded-lg p-4 text-white">
                  <p>No Pokemon owned yet</p>
                  <p className="text-sm text-gray-400">Start collecting Pokemon from the Available Pokemon tab!</p>
                </div>
              </div>
            </div>
          </div>
        )}

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
