import { Metaplex, keypairIdentity } from "@metaplex-foundation/js"
import { Connection, clusterApiUrl, Keypair, PublicKey } from "@solana/web3.js"
import fs from "fs"
import os from "os"

// Load keypair from Solana CLI default location
const keypairPath = `${os.homedir()}/.config/solana/id.json`
const secretKey = Uint8Array.from(JSON.parse(fs.readFileSync(keypairPath, "utf-8")))
const keypair = Keypair.fromSecretKey(secretKey)

// Connect to Solana Devnet
const connection = new Connection(clusterApiUrl("devnet"))
const metaplex = Metaplex.make(connection).use(keypairIdentity(keypair))

// NFT mint address you want to delete
const mintAddress = new PublicKey("9JzFuBfN4Auk7HNCRvhumt2PnMx2BBZapqUtMvq6aFp6")

async function deleteNFT() {
   try {
      // First verify the account exists and is a mint
      const accountInfo = await connection.getAccountInfo(mintAddress)
      if (!accountInfo) {
         throw new Error("Account not found at the provided address")
      }

      const nft = await metaplex.nfts().findByMint({ mintAddress })
      if (!nft) {
         throw new Error("NFT not found at the provided mint address")
      }
      console.log("🔍 Found NFT:", nft.name)

      const { response } = await metaplex.nfts().delete({ mintAddress })
      console.log("✅ NFT deleted successfully.")
      console.log("Transaction Signature:", response.signature)
   } catch (err) {
      console.error("❌ Error deleting NFT:", err)
   }
}

deleteNFT()
