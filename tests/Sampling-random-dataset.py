import os
import glob
import pandas as pd


def combine_csv_files(directory, output_file):
    # Get a list of all CSV files in the directory
    csv_files = glob.glob(os.path.join(directory, '*.csv'))

    # Combine CSV files with an identifier column
    df_list = []
    for file in csv_files:
        temp_df = pd.read_csv(file)
        temp_df['source_file'] = os.path.basename(file)  # Add a column for the source file
        df_list.append(temp_df)

    combined_df = pd.concat(df_list)

    # Save the combined DataFrame to the specified output file
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV file saved to {output_file}")


def sample_proportionately(input_file, output_file, total_sample_size=200):
    # Load the combined CSV file with the source file identifier
    combined_df = pd.read_csv(input_file)

    # Determine the number of unique sources (files)
    unique_sources = combined_df['source_file'].nunique()

    # Calculate the number of rows to sample per file
    rows_per_file = total_sample_size // unique_sources  # Integer division

    # Sample proportionately from each group (each source file)
    sampled_df = combined_df.groupby('source_file').apply(
        lambda x: x.sample(n=rows_per_file, random_state=42)).reset_index(drop=True)

    # Handle any remaining rows (due to integer division)
    remaining_rows = total_sample_size - len(sampled_df)
    if remaining_rows > 0:
        additional_sample = combined_df.drop(sampled_df.index).sample(n=remaining_rows, random_state=42)
        sampled_df = pd.concat([sampled_df, additional_sample])

    # Save the sampled DataFrame to the specified output file
    sampled_df.to_csv(output_file, index=False)
    print(f"Sampled data saved to {output_file}")


def main():
    # Specify the directory and file paths
    directory = '/mnt/d/indus-finetuned-datasets/Final-indus3-cleaned-v1'
    combined_output_file = '/mnt/d/indus-finetuned-datasets/combine-datasets/Indus_Testing_with_source.csv'
    sampled_output_file = '/mnt/d/indus-finetuned-datasets/combine-datasets/Indus_Testing_sampled_file.csv'

    # Combine CSV files and save to the specified output file
    #combine_csv_files(directory, combined_output_file)


    # Call the function to sample proportionately and save to the output file
    sample_proportionately(combined_output_file, sampled_output_file, total_sample_size=150)


if __name__ == "__main__":
    main()


