import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { Pokemon } from "../target/types/pokemon";
import {
  createMint,
  getOrCreateAssociatedTokenAccount,
  mintTo,
} from "@solana/spl-token";
import { PublicKey, SystemProgram } from "@solana/web3.js";
import {
  CreateMetadataAccountV3InstructionData,
  MPL_TOKEN_METADATA_PROGRAM_ID
} from "@metaplex-foundation/mpl-token-metadata";

describe("pokemon", () => {
  const TOKEN_METADATA_PROGRAM_ID = new PublicKey(
    "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
  );

  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);
  const program = anchor.workspace.Pokemon as Program<Pokemon>;

  it("mints an NFT!", async () => {
    // Extract the payer and keypair for signing
    const payer = provider.wallet;
    const payerKeypair = (payer as any).payer; // Assumes NodeWallet with a 'payer' property
    const connection = provider.connection;

    console.log("Payer Public Key:", payer.publicKey.toBase58());
    console.log("Payer Keypair provided:", payerKeypair ? "Yes" : "No");

    // 1. Create a new mint (NFT, 0 decimals)
    console.log("Creating a new mint...");
    const mint = await createMint(
      connection,
      payerKeypair,  // Updated: use keypair here
      payer.publicKey,
      null,
      0
    );
    console.log("Mint created. Mint Address:", mint.toBase58());

    // 2. Get associated token account (ATA)
    console.log("Getting or creating associated token account (ATA)...");
    const tokenAccount = await getOrCreateAssociatedTokenAccount(
      connection,
      payerKeypair,  // Updated: use keypair here
      mint,
      payer.publicKey
    );
    console.log("Token Account Address:", tokenAccount.address.toBase58());

    // 3. Mint 1 token to the ATA
    console.log("Minting 1 token to the ATA...");
    const mintToSignature = await mintTo(
      connection,
      payerKeypair,  // Updated: use keypair here
      mint,
      tokenAccount.address,
      payerKeypair,  // Using the signing keypair
      1
    );
    console.log("Minting complete. MintTo Transaction Signature:", mintToSignature);

    // 4. Derive metadata account PDA
    console.log("Deriving metadata PDA...");
    const [metadataPDA] = await PublicKey.findProgramAddressSync(
      [
        Buffer.from("metadata"),
        TOKEN_METADATA_PROGRAM_ID.toBuffer(),
        mint.toBuffer()
      ],
      TOKEN_METADATA_PROGRAM_ID
    );
    console.log("Metadata PDA:", metadataPDA.toBase58()); //derived metadata account, should not exist yet.

    // 5. Call your Anchor program to handle metadata creation
    console.log("Calling Anchor program to create metadata...");

    try {
      const txSignature = await program.methods
        .mint(
          "Charizard NFT Sample",
          "PKMN",
          "https://aghdifxte3cxyuqmo2yuyrt773y264lo2pwz2drwjvy2bnx45u7q.arweave.net/AY40FvMmxXxSDHaxTEZ__vGvcW7T7Z0ONk1xoLb87T8"
        )
        .accounts({
          payer: payer.publicKey,
          mint,
          metadata: metadataPDA,
          tokenMetadataProgram: TOKEN_METADATA_PROGRAM_ID,
        })
        .signers([payerKeypair])
        .rpc();

      console.log("Anchor program call completed. Transaction Signature:", txSignature);
    } catch (err) {
      console.error("🚨 Anchor program call failed:");
      console.error(err);

      // Optional: pretty print logs
      if ((err as any).logs) {
        console.error("🔍 Transaction logs:");
        for (const log of (err as any).logs) {
          console.error(log);
        }
      }
    }

   

    console.log("✅ Minted NFT! Mint address:", mint.toBase58());
  }, 200000);
});
