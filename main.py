from paper.ai_info_adder.run_ai_idea import run_add_ai_idea
from paper.analysis.run_keyword_analysis import run_analysis_keyword
from paper.meta_adder.run_meta_adder import meta_adder_run
from paper.paper_downloader.run_downloader import run_paper_downloader

def main():
    """
    Get paper meta data, paper text by titles.
    Use Ai to add paper information
    Analyze paper keywords,calculate center bewteeeness.
    
    You just need 
    1. In data/paper.db,use navicate to create a table and fill titles
    2. Change .env.template to .env, and set PAPER_TABLE and MODEL,AI API_KEY
    """
    meta_adder_run()
    run_paper_downloader()
    run_add_ai_idea()
    run_analysis_keyword()
    
if __name__ == "__main__":
    main()