use anchor_lang::prelude::*;

//For defining metadata account on metaplex
use mpl_token_metadata::{
    instructions::CreateMetadataAccountV3Builder,
    instructions::CreateMasterEditionV3Builder,
    types::DataV2,
    ID as MPL_METADATA_ID,
    instructions::BurnNftBuilder
};

// For sending the instruction 
use anchor_lang::solana_program::{
    program::invoke_signed,
    instruction::Instruction,
    system_program
};

use anchor_spl::token::{Token, ID as TOKEN_PROGRAM_ID};


declare_id!("6X7Dmx74WDrQtTRqaGZykdRvLh9LTCwR9WPQKtoJpNSE"); 

#[program]
pub mod pokemon {
    use super::*;

    pub fn mint(
        ctx: Context<MintNft>, 
        metadata_title: String, 
        metadata_symbol: String, 
        metadata_uri: String,
        pokemon_name: String

    ) -> Result<()> {
        let mint_key = ctx.accounts.mint.key();

        let (metadata_pda, _bump) = Pubkey::find_program_address(
        &[
            b"metadata",
            MPL_METADATA_ID.as_ref(),
            mint_key.as_ref(),
        ],
        &MPL_METADATA_ID,
    );

    let (master_edition_pda, _edition_bump) = Pubkey::find_program_address(
        &[
            b"metadata",
            MPL_METADATA_ID.as_ref(),
            mint_key.as_ref(),
            b"edition",
        ],
        &MPL_METADATA_ID,
    );
    
    let pokemon_metadata = DataV2 {
        name: metadata_title,
        symbol: metadata_symbol,
        uri: metadata_uri,
        seller_fee_basis_points: 0,
        creators: None,
        collection: None,
        uses: None,
    };

    let acc = ctx.accounts; //for readability
    let builder = CreateMetadataAccountV3Builder::new()
        .metadata(metadata_pda)
        .mint(acc.mint.key())
        .mint_authority(acc.payer.key())
        .update_authority(acc.payer.key(), true)
        .payer(acc.payer.key())
        .data(pokemon_metadata)
        .is_mutable(true)
        .instruction();

    invoke_signed(
    &builder,
       &[
        acc.metadata.to_account_info(),
        acc.mint.to_account_info(),
        acc.payer.to_account_info(),
        acc.payer.to_account_info(), // update authority is also payer
        acc.system_program.to_account_info(),
        acc.rent.to_account_info(),
        acc.token_metadata_program.to_account_info(),
    ],
    &[], // no signer seeds? unless using PDA mint authority
)?;

let master_edition_ix = CreateMasterEditionV3Builder::new()
        .edition(master_edition_pda)
        .mint(acc.mint.key())
        .update_authority(acc.payer.key())
        .mint_authority(acc.payer.key())
        .payer(acc.payer.key())
        .metadata(metadata_pda)
        .max_supply(0)
        .instruction();

    invoke_signed(
        &master_edition_ix,
        &[
            acc.master_edition.to_account_info(),
            acc.mint.to_account_info(),
            acc.payer.to_account_info(),
            acc.payer.to_account_info(),
            acc.metadata.to_account_info(),
            acc.system_program.to_account_info(),
            acc.token_metadata_program.to_account_info(),
        ],
        &[],
    )?;

    // let counter = &mut acc.mint_counter;
    // let current_count = counter.count;
    // counter.count += 1;
    
    // msg!("Minting {} NFT number {}", pokemon_name, current_count + 1);

    Ok(())
    }

    // pub fn init_mint_counter(
    //     ctx: Context<InitMintCounter>,
    //     pokemon_name: String,
    //     max_supply: u64,
    // ) -> Result<()> {
    //     // let counter = &mut ctx.accounts.mint_counter;
    //     // counter.count = 0;
    //     // counter.max_supply = max_supply;

    //     msg!("Initialized mint counter for {} with max supply {}", pokemon_name, max_supply);
    //     Ok(())
    // }

    // pub fn burn_nft(ctx: Context<BurnNft>, pokemon_name: String) -> Result<()> {

    // let acc = &ctx.accounts;

    // let burn_ix = BurnNftBuilder::new()
    //     .metadata(acc.metadata.key())
    //     .owner(acc.authority.key())
    //     .mint(acc.mint.key())
    //     .token_account(acc.token_account.key())
    //     .master_edition_account(acc.master_edition.key())
    //     .instruction();

    // invoke_signed(
    //     &burn_ix,
    //     &[
    //         acc.metadata.to_account_info(),
    //         acc.authority.to_account_info(),
    //         acc.mint.to_account_info(),
    //         acc.token_account.to_account_info(),
    //         acc.master_edition.to_account_info(),
    //         acc.token_program.to_account_info(),
    //         acc.token_metadata_program.to_account_info(),
    //     ],
    //     &[],
    // )?;

    // Safely decrement the count
    // let counter = &mut ctx.accounts.mint_counter;
    // require!(counter.count > 0, BurnError::NothingToDecrement);
    // counter.count -= 1;

    // msg!("Burned {} NFT. Remaining: {}", pokemon_name, counter.count);

//     Ok(())
// }

}
// do not delete the triple comments --- those are checks used by anchor
#[derive(Accounts)]
#[instruction(pokemon_name: String)]
pub struct MintNft<'info> {
    #[account(mut)]
    pub payer: Signer<'info>,

    /// CHECK: mint
    #[account(mut)]
    pub mint: UncheckedAccount<'info>,

    /// CHECK: metadata account PDA - we'll derive it later
    #[account(mut)]
    pub metadata: UncheckedAccount<'info>,

    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,

    /// CHECK: Metaplex Token Metadata program
    pub token_metadata_program: UncheckedAccount<'info>,

    /// CHECK: Master Edition account PDA
    #[account(mut)]
    pub master_edition: UncheckedAccount<'info>,

    /// CHECK: Metaplex!
    pub token_program: Program<'info, Token>,

    // #[account(
    //     mut,
    //     seeds = [b"mint_counter", pokemon_name.as_bytes()],
    //     bump,
    // )]
    // pub mint_counter: Account<'info, MintCounter>,

}

// #[derive(Accounts)]
// #[instruction(pokemon_name: String)]
// pub struct InitMintCounter<'info> {

//     #[account(init,
//     payer = payer,
//     space = MintCounter::INIT_SPACE,
//     seeds = [b"mint_counter", pokemon_name.as_bytes()],
//     bump,
//     )]
//     pub mint_counter: Account<'info, MintCounter>,


//     #[account(mut)]
//     pub payer: Signer<'info>,
//     pub system_program: Program<'info, System>,

 
// }

// #[account]
// #[derive(InitSpace)]
// pub struct MintCounter {
//     pub count: u64,
//     pub max_supply: u64,
// }


#[derive(Accounts)]
#[instruction(pokemon_name: String)]
pub struct BurnNft<'info> {
    #[account(mut)]
    pub authority: Signer<'info>, // NFT holder

    /// CHECK: NFT mint
    #[account(mut)]
    pub mint: UncheckedAccount<'info>,

    /// CHECK: NFT token account (owned by authority)
    #[account(mut)]
    pub token_account: UncheckedAccount<'info>,

    /// CHECK: Metadata PDA
    #[account(mut)]
    pub metadata: UncheckedAccount<'info>,

    /// CHECK: Master edition PDA
    #[account(mut)]
    pub master_edition: UncheckedAccount<'info>,

    /// CHECK: Metaplex Token Metadata Program
    pub token_metadata_program: UncheckedAccount<'info>,

    /// SPL Token Program
    pub token_program: Program<'info, Token>,

    // #[account(
    //     mut,
    //     seeds = [b"mint_counter", pokemon_name.as_bytes()],
    //     bump
    // )]
    // pub mint_counter: Account<'info, MintCounter>,
}

// #[error_code]
// pub enum BurnError {
//     #[msg("Counter is already zero, can't decrement.")]
//     NothingToDecrement,
// }