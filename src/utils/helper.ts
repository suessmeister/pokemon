import { Connection, PublicKey } from '@solana/web3.js';
import { Metaplex } from '@metaplex-foundation/js';

export async function getNftsForWallet(walletAddress: PublicKey, connection: Connection) {
   try {
      const metaplex = new Metaplex(connection);
      const nfts = await metaplex
         .nfts()
         .findAllByOwner({ owner: walletAddress });

      // Filter for Pokemon NFTs (PKMN symbol)
      const pokemonNfts = nfts.filter(nft =>
         nft.symbol === 'PKMN' || nft.symbol === 'pkmn'
      );

      // Fetch metadata for each NFT
      const nftsWithMetadata = await Promise.all(
         pokemonNfts.map(async (nft) => {
            try {
               const response = await fetch(nft.uri);
               const metadata = await response.json();
               return {
                  name: nft.name,
                  symbol: nft.symbol,
                  image: metadata.image,
                  description: metadata.description || '',
                  mint: nft.address.toString(),
               };
            } catch (error) {
               console.error('Error fetching metadata:', error);
               return null;
            }
         })
      );

      return nftsWithMetadata.filter(Boolean);
   } catch (error) {
      console.error('Error fetching NFTs:', error);
      return [];
   }
}
