'use client'

import Image from 'next/image'
import { useState, useEffect } from 'react'
import { WalletButton } from '@/components/solana/solana-provider'
import { useWallet } from '@solana/wallet-adapter-react'
import { Connection, LAMPORTS_PER_SOL, PublicKey, Keypair, SystemProgram, SYSVAR_RENT_PUBKEY, clusterApiUrl } from '@solana/web3.js'
import pokemonData from '@/data/pokemon.json'
import shiningData from '@/data/shining.json'
import mappings from '@/data/mappings.json'
import { getNftsForWallet } from '@/utils/helper'

// SPL Token & Anchor Imports
import * as anchor from "@coral-xyz/anchor";
import { Program, web3 } from "@coral-xyz/anchor";
import {
   createMint,
   getOrCreateAssociatedTokenAccount,
   mintTo,
   TOKEN_PROGRAM_ID,
} from "@solana/spl-token";
import idl from "../../../anchor/target/idl/pokemon.json"
import { Pokemon } from 'anchor/target/types/pokemon'

// Metaplex Metadata Program ID
const TOKEN_METADATA_PROGRAM_ID = new PublicKey(
   "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
);

export default function Collection() {
   const [imageError, setImageError] = useState<{ [key: string]: boolean }>({})
   const [activeTab, setActiveTab] = useState<'available' | 'owned'>('available')
   const { publicKey, disconnect, sendTransaction, wallet } = useWallet()
   const [balance, setBalance] = useState<number>(0)
   const [ownedNFTs, setOwnedNFTs] = useState<any[]>([])

   // --- Setup Connection, Provider, and Program ---
   const connection = new Connection(clusterApiUrl('devnet'), "confirmed");
   const provider = new anchor.AnchorProvider(connection, wallet as any, {
      preflightCommitment: "processed",
   });
   anchor.setProvider(provider);

   //include the provider
   const program: anchor.Program<Pokemon> = new Program(idl as Pokemon, { connection })

   // --- Load Balance ---
   useEffect(() => {
      async function getBalance() {
         if (!publicKey) return
         try {
            const balance = await connection.getBalance(publicKey)
            setBalance(balance / LAMPORTS_PER_SOL)
         } catch (error) {
            console.error('Error fetching balance:', error)
         }
      }
      getBalance()
   }, [publicKey])

   // --- Load Owned NFTs ---
   useEffect(() => {
      async function fetchOwnedNFTs() {
         if (!publicKey) return
         try {
            const nfts = await getNftsForWallet(publicKey, connection)
            setOwnedNFTs(nfts)
         } catch (err) {
            console.error('Error fetching NFTs:', err)
         }
      }
      fetchOwnedNFTs()
   }, [publicKey])

   const buyPack = async () => {
      if (!publicKey) return alert("Connect your wallet first")

      try {
         // === Step 1. Charge Fee ===
         const treasuryPubkey = new PublicKey("8rrF7VycfSHR48iQ7HXTRwHaNJNf2p2MkA5fHf5KDSJ")
         const feeLamports = 0.05 * LAMPORTS_PER_SOL

         const feeTx = new web3.Transaction().add(
            web3.SystemProgram.transfer({
               fromPubkey: publicKey,
               toPubkey: treasuryPubkey,
               lamports: feeLamports,
            })
         )
         const feeSignature = await sendTransaction(feeTx, connection)
         await connection.confirmTransaction(feeSignature, "processed")

         // === Step 2. Choose a Random Pokémon NFT Data ===
         const pokemons = mappings.pokemon
         const randomPokemon = pokemons[1]  // For testing, using a hardcoded index

         // === Step 3. Mint the NFT on-chain ===
         const mintKeypair = Keypair.generate()
         const mint = mintKeypair.publicKey

         // Derive PDAs
         const [metadataPDA] = PublicKey.findProgramAddressSync(
            [Buffer.from("metadata"), TOKEN_METADATA_PROGRAM_ID.toBuffer(), mint.toBuffer()],
            TOKEN_METADATA_PROGRAM_ID
         )
         const [masterEditionPDA] = PublicKey.findProgramAddressSync(
            [Buffer.from("metadata"), TOKEN_METADATA_PROGRAM_ID.toBuffer(), mint.toBuffer(), Buffer.from("edition")],
            TOKEN_METADATA_PROGRAM_ID
         )

         // Call the Anchor program's mint instruction
         const mintSignature = await program.methods
            .mint(
               randomPokemon.name,
               "PKMN",
               randomPokemon.metadata_link,
               randomPokemon.name
            )
            .accounts({
               payer: publicKey,
               mint: mint,
               metadata: metadataPDA,
               masterEdition: masterEditionPDA,
               tokenMetadataProgram: TOKEN_METADATA_PROGRAM_ID,
            })
            .signers([mintKeypair])
            .rpc()

         console.log("✅ Anchor call succeeded. Tx signature:", mintSignature)
         console.log("🎉 NFT Minted! Mint address:", mint.toBase58())
         alert(`🎉 You got ${randomPokemon.name}! NFT minted successfully.`)

         setTimeout(() => window.location.reload(), 5000)
      } catch (err) {
         console.error("Buy pack failed", err)
         if ((err as any).logs) {
            console.error("Transaction logs:")
            for (const log of (err as any).logs) {
               console.error(log)
            }
         }
         alert("Transaction failed. Try again!")
      }
   }

   return (
      <main className="min-h-screen p-8 bg-gradient-to-b from-blue-500 to-blue-700">
         <div className="max-w-6xl mx-auto">
            {/* Header with wallet */}
            <div className="flex justify-between items-center mb-8">
               <h1 className="text-4xl font-bold text-yellow-300 pokemon-title">
                  Pokémon Collection
               </h1>
               {publicKey ? (
                  <div className="flex items-center gap-4">
                     <div className="text-white bg-black/20 px-4 py-2 rounded-lg">
                        {balance.toFixed(2)} SOL
                     </div>
                     <button
                        onClick={disconnect}
                        className="btn !bg-white !text-black hover:!bg-gray-100"
                     >
                        Disconnect
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
                     Connect your wallet to start collecting Pokémon NFTs!
                  </p>
               </div>
            )}

            {/* Tab Navigation with Buy Pack button */}
            {publicKey && (
               <div className="flex justify-center mb-8 gap-2">
                  <button
                     onClick={() => setActiveTab('available')}
                     className={`px-6 py-2 rounded-md transition-colors ${activeTab === 'available'
                        ? 'bg-yellow-300 text-black'
                        : 'text-white hover:bg-black/30'
                        }`}
                  >
                     Available Pokémon
                  </button>
                  <button
                     onClick={() => setActiveTab('owned')}
                     className={`px-6 py-2 rounded-md transition-colors ${activeTab === 'owned'
                        ? 'bg-yellow-300 text-black'
                        : 'text-white hover:bg-black/30'
                        }`}
                  >
                     My Pokémon
                  </button>
                  <button
                     onClick={buyPack}
                     className="px-6 py-2 rounded-md transition-colors bg-yellow-300 text-black hover:bg-yellow-400"
                  >
                     Buy Pack (0.05 SOL)
                  </button>
               </div>
            )}

            {/* Available Pokémon Section */}
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
                                    onError={() =>
                                       setImageError((prev) => ({ ...prev, [poke.name]: true }))
                                    }
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

                  {/* Shining Pokémon Section */}
                  <div className="mt-16">
                     <h1 className="text-5xl font-bold text-yellow-300 pokemon-title mb-8 text-center">
                        Shining Pokémon
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
                                       onError={() =>
                                          setImageError((prev) => ({
                                             ...prev,
                                             [`shiny-${poke.name}`]: true
                                          }))
                                       }
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

            {/* Owned Pokémon Section */}
            {activeTab === 'owned' && publicKey && (
               <div className="text-center">
                  <div className="bg-black/20 rounded-lg p-8">
                     <h2 className="text-2xl font-bold text-yellow-300 mb-4">
                        Your Pokémon Collection
                     </h2>
                     <p className="text-white mb-2">Showing Pokémon for wallet:</p>
                     <p className="text-yellow-300 font-mono text-sm mb-4 break-all">
                        {publicKey.toString()}
                     </p>
                     <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {ownedNFTs.length > 0 ? (
                           ownedNFTs.map((nft, idx) => (
                              <div
                                 key={idx}
                                 className="bg-black/30 rounded-lg p-4 text-white transform hover:scale-105 transition-transform"
                              >
                                 <img src={nft.image} alt={nft.name} className="rounded" />
                                 <h3 className="mt-2 text-xl font-bold text-yellow-300">
                                    {nft.name}
                                 </h3>
                                 <p className="text-sm text-gray-400">
                                    {nft.description}
                                 </p>
                              </div>
                           ))
                        ) : (
                           <div className="bg-black/30 rounded-lg p-4 text-white">
                              <p>No Pokémon NFTs found in your wallet.</p>
                              <p className="text-sm text-gray-400">
                                 Start collecting Pokémon from the Available tab!
                              </p>
                           </div>
                        )}
                     </div>
                  </div>
               </div>
            )}
         </div>
      </main>
   )
} 