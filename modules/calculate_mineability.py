def calculate_mineability(combined_df, preserve_list, obtain_list, output_file):

    # Calculate the mineability of each cell
    combined_df["mineability"] = combined_df[obtain_list].fillna(0).sum(axis=1)

    # Preserve the cells that contain the materials in the preserve list or if the value is empty (we don't want to take chances)
    for material in preserve_list:
        combined_df.loc[(combined_df[material] > 0) | (combined_df[material].isna()), "mineability"] = 0

    # Save the mineability data to a new CSV file
    combined_df.to_csv(output_file, index=False)

    return combined_df