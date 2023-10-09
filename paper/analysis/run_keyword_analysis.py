
import pandas as pd
import os
import sys
import sqlite3

sys.path.append(os.getcwd())
from paper.analysis.processing_keyword import *
from paper.analysis.co_occurrence import *
from paper.analysis.network_analysis import *



def run_analysis_keyword():
    print("start analysis keyword")
    conn = sqlite3.connect('data/paper.db')

    # read data
    paper_df = read_paper_table()
    
    # Get the keyword table as the basic table
    paper_df = extract_keyword(paper_df)
    paper_keyword_df = build_paper_keyword_table(paper_df)

    # Get the importance of keywrod by network analysis
    co_keyword_occurrence_matrix = build_keyword_co_matrix(paper_keyword_df)
    keyword_indicator_df  = get_keyword_network_indicator(co_keyword_occurrence_matrix)

    # Get keyword by various occurence years
    keyword_time_df = build_keyword_time_table(paper_keyword_df)
    
    # Merge the years and importance of keyword
    keyword_time_indicator_df = merge_importance_year(keyword_indicator_df, keyword_time_df)
    keyword_time_indicator_df.to_sql(f'{PAPER_TABLE}_keyword_analysis', conn, if_exists='replace', index=False)
    
    print("keyword analysis done")

if __name__ == "__main__":
    run_analysis_keyword()