import numpy as np
import pandas as pd
from tqdm import tqdm
import os
import sys
sys.path.append(os.getcwd())


def build_keyword_co_matrix(paper_keyword_df):
    '''
    
    '''
    # 拿到所有的关键词,标题
    unique_keywords = paper_keyword_df['keyword'].unique()

    # 创建关键词到索引的映射
    # 也就是 {keyword:idx}的编号
    unique_keywords_map = {keyword: idx for idx, keyword in enumerate(unique_keywords)}
    
    # 获得每篇文章的关键词列表
    keywords_serise = paper_keyword_df.groupby('title')['keyword'].apply(list)

    # 计算共现矩阵
    matrix_shape = (len(unique_keywords), len(unique_keywords))
    co_occurrence_matrix = compute_co_occurrence_numpy(keywords_serise, unique_keywords_map, matrix_shape)
   
    # 对角线为0
    np.fill_diagonal(co_occurrence_matrix, 0)

    # 转换为DataFrame
    co_occurrence_matrix_df = pd.DataFrame(co_occurrence_matrix, index=unique_keywords, columns=unique_keywords)

    return co_occurrence_matrix_df


def compute_co_occurrence_numpy(keywords_serise, unique_keywords_map, matrix_shape):
    '''
    Compute cooccurence matrix
    Use numpy to speed up calulate.So,use index to map keyword
    '''
    co_occurrence_matrix = np.zeros(matrix_shape, dtype=np.int64)
    
    for keywords in keywords_serise.values:
        indices = [unique_keywords_map[key] for key in keywords] # 拿到关键词,对应的索引

        for i in range(len(indices)): # 对于每个文章关键词的列表,进行遍历,统计共现次数.并且把关键词索引,放到共现矩阵中
            for j in range(i+1, len(indices)):
                row = indices[i]
                col = indices[j]
                co_occurrence_matrix[row, col] += 1
                co_occurrence_matrix[col, row] += 1
                
    return co_occurrence_matrix