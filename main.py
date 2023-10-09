from paper.ai_info_adder import run_ai_idea
from paper.analysis import run_keyword_analysis
from paper.meta_adder import run_meta_adder
from paper.paper_downloader import run_downloader

def main():
    """
    Get paper meta data, paper text by titles.
    Use Ai to add paper information
    Analyze paper keywords,calculate center bewteeeness.
    
    You just need 
    1. In data/paper.db,use navicate to create a table and fill titles
    2. Change .env.template to .env, and set PAPER_TABLE and MODEL,AI API_KEY
    """
    run_ai_idea()
    run_meta_adder()
    run_downloader()
    run_keyword_analysis()
    
if __name__ == "__main__":
    main()