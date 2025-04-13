'use client';

import { useState } from 'react';
import { useWallet } from '@solana/wallet-adapter-react';
import { Connection, PublicKey, LAMPORTS_PER_SOL, SystemProgram } from '@solana/web3.js';
import { Program } from '@coral-xyz/anchor';
import { TOKEN_PROGRAM_ID } from '@solana/spl-token';
import { getNftsForWallet } from '@/utils/helper';
import pokemonData from '@/data/pokemon.json';
import shiningData from '@/data/shining.json';

interface NFTDisplayProps {
   publicKey: PublicKey | null;
   ownedNFTs: any[];
   activeTab: 'available' | 'owned';
   onTabChange: (tab: 'available' | 'owned') => void;
   connection: Connection;
   program: Program;
   onNFTsUpdate: (nfts: any[]) => void;
}

export default function NFTDisplay({
   publicKey,
   ownedNFTs,
   activeTab,
   onTabChange,
   connection,
   program,
   onNFTsUpdate,
}: NFTDisplayProps) {
   const { sendTransaction } = useWallet();
   const [isLoading, setIsLoading] = useState(false);
   const [error, setError] = useState<string | null>(null);

   const buyCardPack = async () => {
      if (!publicKey || !program) return;

      setIsLoading(true);
      setError(null);

      try {
         // Pay the pack fee (0.1 SOL)
         const packFee = 0.1 * LAMPORTS_PER_SOL;
         const treasuryWallet = new PublicKey("YOUR_TREASURY_WALLET_PUBLIC_KEY_HERE"); // Replace with your treasury wallet

         const feeTx = SystemProgram.transfer({
            fromPubkey: publicKey,
            toPubkey: treasuryWallet,
            lamports: packFee,
         });

         const feeSignature = await sendTransaction(feeTx, connection);
         await connection.confirmTransaction(feeSignature);

         // Select a random Pokémon
         const randomIndex = Math.floor(Math.random() * pokemonData.length);
         const selectedPokemon = pokemonData[randomIndex];
         const isShining = Math.random() < 0.1; // 10% chance of being shining

         // Create mint
         const mint = new PublicKey(selectedPokemon.mint);

         // Get metadata PDA
         const [metadataPDA] = PublicKey.findProgramAddressSync(
            [
               Buffer.from('metadata'),
               TOKEN_METADATA_PROGRAM_ID.toBuffer(),
               mint.toBuffer(),
            ],
            TOKEN_METADATA_PROGRAM_ID
         );

         // Get master edition PDA
         const [masterEditionPDA] = PublicKey.findProgramAddressSync(
            [
               Buffer.from('metadata'),
               TOKEN_METADATA_PROGRAM_ID.toBuffer(),
               mint.toBuffer(),
               Buffer.from('edition'),
            ],
            TOKEN_METADATA_PROGRAM_ID
         );

         // Call mint instruction
         const tx = await program.methods
            .mint(
               selectedPokemon.name,
               'PKMN',
               isShining ? shiningData[selectedPokemon.id] : selectedPokemon.image,
               selectedPokemon.name
            )
            .accounts({
               payer: publicKey,
               mint,
               metadata: metadataPDA,
               masterEdition: masterEditionPDA,
               tokenMetadataProgram: TOKEN_METADATA_PROGRAM_ID,
            })
            .transaction();

         const signature = await sendTransaction(tx, connection);
         await connection.confirmTransaction(signature);

         // Update owned NFTs
         const updatedNFTs = await getNftsForWallet(publicKey, connection);
         onNFTsUpdate(updatedNFTs);
      } catch (err) {
         console.error('Error buying card pack:', err);
         setError('Failed to buy card pack. Please try again.');
      } finally {
         setIsLoading(false);
      }
   };

   return (
      <div className="mt-8">
         <div className="flex space-x-4 mb-4">
            <button
               className={`px-4 py-2 rounded ${activeTab === 'available'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700'
                  }`}
               onClick={() => onTabChange('available')}
            >
               Available Pokemon
            </button>
            <button
               className={`px-4 py-2 rounded ${activeTab === 'owned'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700'
                  }`}
               onClick={() => onTabChange('owned')}
            >
               My Pokemon
            </button>
         </div>

         {activeTab === 'owned' && (
            <div className="mb-4">
               <button
                  className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50"
                  onClick={buyCardPack}
                  disabled={isLoading || !publicKey}
               >
                  {isLoading ? 'Opening Pack...' : 'Buy Card Pack (0.1 SOL)'}
               </button>
               <p className="text-sm text-gray-600 mt-1">
                  Get a random Pokémon with a 10% chance of being shining!
               </p>
            </div>
         )}

         {error && (
            <div className="mb-4 p-2 bg-red-100 text-red-700 rounded">
               {error}
            </div>
         )}

         <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {ownedNFTs.map((nft) => (
               <div
                  key={nft.mint}
                  className="p-4 border rounded-lg shadow hover:shadow-lg transition-shadow"
               >
                  <img
                     src={nft.image}
                     alt={nft.name}
                     className="w-full h-48 object-contain mb-2"
                  />
                  <h3 className="text-lg font-semibold">{nft.name}</h3>
                  <p className="text-sm text-gray-600">Mint: {nft.mint}</p>
               </div>
            ))}
         </div>
      </div>
   );
} 