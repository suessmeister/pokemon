use anchor_lang::prelude::*;

//For defining metadata account on metaplex
use mpl_token_metadata::{
    instructions::CreateMetadataAccountV3Builder,
    types::DataV2,
    ID as MPL_METADATA_ID
};

// For sending the instruction 
use anchor_lang::solana_program::{
    program::invoke_signed,
    instruction::Instruction,
    system_program
};

declare_id!("6X7Dmx74WDrQtTRqaGZykdRvLh9LTCwR9WPQKtoJpNSE"); // program id here

#[program]
pub mod pokemon {
    use super::*;

    pub fn mint(
        ctx: Context<MintNft>, 
        metadata_title: String, 
        metadata_symbol: String, 
        metadata_uri: String,

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


        Ok(())
    }
}

#[derive(Accounts)]
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

}
